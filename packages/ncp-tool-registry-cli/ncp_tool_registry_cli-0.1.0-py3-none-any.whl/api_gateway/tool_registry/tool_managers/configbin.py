import logging
from typing import Dict, Optional

from configbin import CBClient, CBPrefix, create_config
from configbin.deployments import Stack, Env

from api_gateway.models.tool_models import ConfigBinTool, ConfigBinToolConfig

logger = logging.getLogger(__name__)

USER = "fassumpcao@netflix.com"


class ConfigbinManager:
    def __init__(self, configbin_prefix="fassumpcao/tool-registry"):
        self.tool_registry = CBPrefix(config_bin_client=CBClient(stack=Stack.IEP, env=Env.TEST), prefix=configbin_prefix)
        self.tool_registry.sync()

    async def sync_tool_registry(self):
        self.tool_registry.sync()

    def add_tool_to_configbin(self, new_tool: ConfigBinTool, comment: str = "Create tool", user: str = "fassumpcao@netflix.com"):
        try:
            create_config(self.tool_registry, new_tool.tool_id, new_tool.model_dump_json(), user=user, comment=comment)
            logger.info(f"Tool {new_tool.tool_id} successfully added to ConfigBin")
        except Exception as e:
            logger.error(f"Failed to add tool to ConfigBin: {e}")
            raise

    def get_tool_by_id(self, tool_id: str) -> Optional[ConfigBinTool]:
        try:
            config = self.tool_registry.get_from_cache(tool_id)
            if config:
                return ConfigBinTool.model_validate(config.payload)
            return None
        except Exception as e:
            logger.error(f"Failed to get tool {tool_id} from ConfigBin with error: {e}")
            return None

    def list_tools(self) -> Dict[str, ConfigBinToolConfig]:
        return self.tool_registry.configs

    def delete_tool(self, tool_id: str, comment: str = "Delete tool", user: str = "fassumpcao@netflix.com"):
        try:
            self.tool_registry.delete(tool_id, user=user, comment=comment)
            logger.info(f"Tool {tool_id} successfully deleted from ConfigBin")
        except Exception as e:
            logger.error(f"Failed to delete tool from ConfigBin: {e}")
            raise


def get_tool_invocation_path(configbin_tool: ConfigBinTool) -> str:
    path_params = ""
    start = 0
    url = configbin_tool.invocation["endpoint"]
    while True:
        start = url.find("{", start)
        if start == -1:
            break

        end = url.find("}", start)
        if end == -1:
            break

        param = url[start : end + 1]
        path_params += f"/{param}"
        start = end + 1

    return f"/ncp_model_gateway/v1/function/{configbin_tool.tool_id}/invoke{path_params}"
