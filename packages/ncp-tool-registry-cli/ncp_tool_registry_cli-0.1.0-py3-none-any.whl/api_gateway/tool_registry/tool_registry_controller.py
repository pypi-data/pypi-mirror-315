import json
import logging
from typing import Dict
import requests

from fastapi import APIRouter, Query, HTTPException

from api_gateway.gateway_service import process_schema
from api_gateway.models.tool_models import ConfigBinTool, CreateToolRequest, ConfigBinToolConfig
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from api_gateway.tool_registry.utils.discovery import discover_openapi, get_app_name, get_endpoint_schemas_and_components
from api_gateway.tool_registry.utils.validators import is_valid_id, is_valid_jsonpath


logger = logging.getLogger(__name__)

router = APIRouter()

configbinManager = ConfigbinManager()


@router.get("/tool_registry", response_model=Dict[str, ConfigBinToolConfig])
async def list_tools() -> Dict[str, ConfigBinToolConfig]:
    return ConfigbinManager().list_tools()


@router.post("/tool_registry/{tool_id}", response_model=ConfigBinTool)
async def register_tool(
    tool_id: str,
    body: CreateToolRequest,
    sync_to_danswer: bool = Query(True, description="Flag to sync the tool to Danswer after registration"),
) -> ConfigBinTool:
    if not is_valid_id(tool_id):
        raise HTTPException(status_code=400, detail="Invalid tool_id! Please use only alphanumeric characters, underscores, and dashes.")

    spec = discover_openapi(body.base_url)
    if not spec:
        raise HTTPException(status_code=400, detail="Could not find OpenAPI docs for provided URL.")

    request_schemas, components, response_schemas = get_endpoint_schemas_and_components(path=body.path, methods=body.methods, spec=spec)

    if body.preprocessing_jsonpath and (
        not is_valid_jsonpath(body.preprocessing_jsonpath) or not process_schema(request_schemas, body.preprocessing_jsonpath)
    ):
        raise HTTPException(status_code=400, detail="Invalid preprocessing_jsonpath")

    if body.postprocessing_jsonpath and (
        not is_valid_jsonpath(body.postprocessing_jsonpath) or not process_schema(response_schemas, body.postprocessing_jsonpath)
    ):
        raise HTTPException(status_code=400, detail="Invalid postprocessing_jsonpath")

    invocation = {"endpoint": body.base_url + body.path}
    if "netflix" in body.base_url:
        invocation["type"] = "metatron_endpoint"
        invocation["app_name"] = get_app_name(body.base_url)

    tool = ConfigBinTool(
        tool_id=tool_id,
        info=body.info,
        response_schema=response_schemas,
        preprocessing_jsonpath=body.preprocessing_jsonpath,
        postprocessing_jsonpath=body.postprocessing_jsonpath,
        permissions={},
        openapi=spec["openapi"],
        request_schema=request_schemas,
        invocation=invocation,
        components=components,
    )
    try:
        ConfigbinManager().add_tool_to_configbin(tool, f"Create tool {tool.tool_id}")
        if sync_to_danswer:
            DanswerToolManager().add_single_tool(tool)
        return tool
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to register tool: {e}")


@router.get("/tool_registry/{tool_id}", response_model=ConfigBinTool)
async def get_tool(tool_id: str) -> ConfigBinTool:
    tool = ConfigbinManager().get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    return tool


@router.delete("/tool_registry/{tool_id}")
async def delete_tool(
    tool_id: str, delete_from_danswer: bool = Query(True, description="Flag to sync the tool to Danswer after registration")
) -> str:
    tool = ConfigbinManager().get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    ConfigbinManager().delete_tool(tool_id, f"Delete tool {tool_id}")
    if delete_from_danswer:
        DanswerToolManager().delete_tool(tool_id)
    return f"Tool {tool_id} successfully deleted."


@router.post("/tool_registry/{tool_id}/sync_to_danswer")
async def sync_tool_to_danswer(tool_id: str) -> str:
    tool = ConfigbinManager().get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
    if DanswerToolManager().add_single_tool(tool):
        return f"Tool {tool_id} successfully synced to Danswer."
    else:
        return f"Tool {tool_id} already present in Danswer."


@router.get("/graphql")
async def graphql(base_url: str):
    introspection_query = """
    query IntrospectionQuery {
      __schema {
        types {
          name
          fields {
            name
            type {
              name
              kind
              ofType {
                name
                kind
              }
            }
          }
        }
      }
    }
    """

    headers = {
        "Content-Type": "application/json",
    }

    payload = {"query": introspection_query}

    try:
        response = requests.post(base_url, json=payload, headers=headers)
        response.raise_for_status()
        schema = response.json()
        print(json.dumps(schema, indent=2))
        return schema
    except requests.exceptions.RequestException as e:
        print(f"Error fetching schema: {e}")
        return None
