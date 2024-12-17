from pydantic import BaseModel
from typing import Dict, Any, List, Literal, Optional


class Info(BaseModel):
    title: str
    description: str
    version: str


class ConfigBinTool(BaseModel):
    tool_id: str
    response_schema: Dict[str, Any]
    postprocessing_jsonpath: Optional[str] = ""
    permissions: Optional[Dict[str, Any]] = {}
    openapi: str
    info: Info
    request_schema: Dict[Literal["post", "get", "delete", "put", "patch"], Dict[str, Any]]
    invocation: Dict[str, Any]
    preprocessing_jsonpath: Optional[str] = ""
    components: Optional[Dict[str, Any]] = {}


class Server(BaseModel):
    url: str = "http://host.docker.internal:4321"
    description: Optional[str] = None


class CustomHeader(BaseModel):
    key: str
    value: str


class DanswerToolDefinition(BaseModel):
    info: Info
    openapi: str
    paths: Dict[str, Any]
    components: Dict[str, Any] | None
    servers: List[Server] = [Server()]  # Default server above


class DanswerTool(BaseModel):
    name: str
    description: str
    definition: DanswerToolDefinition
    custom_headers: List[CustomHeader] = [
        CustomHeader(key="Host", value="p7004.apigateway.vip.us-east-1.test.dns.mesh.netflix.net"),
        CustomHeader(key="Content-Type", value="application/json"),
    ]


class CreateToolRequest(BaseModel):
    info: Info
    base_url: str
    path: str
    methods: List[str]
    preprocessing_jsonpath: Optional[str] = None
    postprocessing_jsonpath: Optional[str] = None


class Version(BaseModel):
    user: str
    comment: str
    hash: str
    prefixVersion: int
    ts: int


class ConfigBinToolConfig(BaseModel):
    name: str
    payload: ConfigBinTool
    version: Version
