import logging
from typing import Any, Dict, Optional

from nflxconfig import NXCONF
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from nflx_security_util import get_authorized_caller
from nflx_security_util.utils import NflxSecurityUtilException
import nflxlog
import nflxtrace
from nflxlog.nflxlogger import NflxLogger
from contextlib import asynccontextmanager
from spectator import GlobalRegistry
from nflxmetrics.fastapi_middleware import MetricsMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api_gateway.gateway_service import invoke_tool, process_schema
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_registry_controller import router as tool_registry_router

NXCONF.defaults.load_config(__file__)
logger = NflxLogger(__name__)

logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
nflxlog.init()
nflxtrace.trace_init()
nflxtrace.instrument_auto()
logging.getLogger().setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.configbin_manager = ConfigbinManager()
        logger.info("Successfully loaded tools from ConfigBin")

    except Exception as e:
        logger.error(f"Failed to initialize ConfigBin: {e}")
        raise

    yield

    app.configbin_manager = None


APP = FastAPI(lifespan=lifespan)

APP.add_middleware(SentryAsgiMiddleware)
APP.add_middleware(MetricsMiddleware)

APP.include_router(tool_registry_router)

nflxtrace.instrument_fastapi_app(APP)


class GenericRequest(BaseModel):
    data: Dict[str, Any]


@APP.api_route("/ncp_model_gateway/v1/function/{tool_id}/invoke", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@APP.api_route("/ncp_model_gateway/v1/function/{tool_id}/invoke/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(tool_id: str, request: Request, body: Optional[GenericRequest] = None, path: str = None):
    tool = APP.configbin_manager.get_tool_by_id(tool_id)
    if not tool:
        await APP.configbin_manager.sync_tool_registry()
        tool = APP.configbin_manager.get_tool_by_id(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail=f"ERROR: Tool not found: {tool_id}")

    logger.info(f"Calling tool: {tool.tool_id}")
    GlobalRegistry.counter("tool_invocation_count", tags={"tool_id": tool_id}).increment()

    try:
        response = await invoke_tool(tool, request, additional_path=path)
        if response:
            logger.info(f"Response: {response.text[:500]}")
        else:
            logger.info("Response: None")
    except Exception as e:
        error_message = f"ERROR! Failed to call tool with exception: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)

    if tool.postprocessing_jsonpath:
        filtered = process_schema(response.json(), tool.postprocessing_jsonpath)
        logger.info(
            "Applied postprocessing: original length was %s and filtered length was %s.", len(str(response.json())), len(str(filtered))
        )
        return filtered

    if response and response.text:
        return response.text
    else:
        # We still want to let the LLM know the tool was successfully called even if there is no response
        return f"Success! Done calling tool: {tool.tool_id}"


@APP.get("/protected")
async def protected(request: Request) -> str:
    """
    Example on how to use nflx-security-util
    for authZ.
    """
    try:
        caller = get_authorized_caller(request)  # extract information about direct/initial caller identity
    except NflxSecurityUtilException as e:
        raise HTTPException(status_code=403, detail=str(e))

    # example for matching direct caller identity type
    if caller.direct.identityType == "User":
        return f"Email: {caller.direct.identity.username}"
        # even more details about a User can be extracted with caller.direct.identity.get_user_details()
    elif caller.direct.identityType == "Application":
        return f"Application Name: {caller.direct.identity.applicationName}"
    else:
        return f"Identity: {caller.direct.identityType}"


@APP.get("/healthcheck")
async def healthcheck() -> str:
    return "OK"


if __name__ == "__main__":
    logger.configure()
    port = NXCONF.get_int("server.port", 7101)
    logger.info(f"Starting server on port {port}")
    uvicorn.run("api_gateway.webapp:APP", host="0.0.0.0", port=port, log_level="info", reload=True)
