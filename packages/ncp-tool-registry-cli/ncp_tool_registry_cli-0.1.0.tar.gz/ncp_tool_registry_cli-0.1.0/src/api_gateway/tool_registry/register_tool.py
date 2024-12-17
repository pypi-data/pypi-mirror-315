import click
from pydantic import ValidationError

from api_gateway.tool_registry.utils.discovery import (
    discover_openapi,
    get_app_name,
    get_endpoint_paths,
    get_path_methods,
    get_endpoint_schemas_and_components,
)
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from api_gateway.tool_registry.utils.validators import is_valid_id, is_valid_jsonpath
from api_gateway.gateway_service import process_schema
from api_gateway.models.tool_models import ConfigBinTool, Info


@click.group()
def cli():
    pass


@cli.command()
def create_tool():
    tool = build_configbintool()
    if tool:
        print("-" * 20)
        print("Uploading tool to ConfigBin...")
        ConfigbinManager().add_tool_to_configbin(tool, f"Create tool {tool.tool_id}")
        print("Done uploading tool to ConfigBin...")
        print("-" * 20)
        danswer_sync = input("Sync tool to Danswer? (y/n): ")
        while danswer_sync.lower() != "y" and danswer_sync.lower() != "n":
            danswer_sync = input("Please enter 'y' or 'n': ")

        if danswer_sync.lower() == "y":
            print("Syncing tool to Danswer...")
            DanswerToolManager().add_single_tool(tool)
            print("Done adding tool to Danswer")

        print("-" * 20)
        print("Tool registration complete!")


def get_info_from_user() -> Info:
    print("\n--- Tool Info ---")
    title = input("Enter title: ").strip()
    description = input("Enter description: ").strip()
    version = input("Enter version: ").strip()
    return Info(title=title, description=description, version=version)


def build_configbintool():
    print("\nLet's register your custom tool! Please provide the following information:")

    tool_id = input("\nEnter tool id: ").strip()
    while not is_valid_id(tool_id):
        print("\nInvalid tool id! Please use only alphanumeric characters, underscores, and dashes.")
        tool_id = input("Enter tool id: ").strip()

    info = get_info_from_user()

    print("\n--- Request Schema ---")
    print("Now we'll generate the request schema using the endpoint discovery flow...")

    base_url = input("Please enter the base URL: ").strip()
    spec = discover_openapi(base_url)
    while not spec:
        print("Couldn't get OpenAPI docs from given URL. Please try another URL.")
        base_url = input("Please enter the base URL: ").strip()
        spec = discover_openapi(base_url)

    openapi = spec["openapi"]

    paths = get_endpoint_paths(spec=spec)
    print("\nAvailable paths:")
    for idx, path in enumerate(paths, 1):
        print(f"{idx}. {path}")

    selected_path = input("\nPlease enter a path or number from the list above: ").strip()
    if selected_path.isdigit() and int(selected_path) <= len(paths):
        selected_path = paths[int(selected_path) - 1]
    else:
        while selected_path not in paths:
            print("\nPath not in list above!")
            selected_path = input("Please enter a path from the list above: ").strip()

    invocation = {}
    if "netflix" in base_url:
        invocation["type"] = "metatron_endpoint"
        invocation["app_name"] = get_app_name(base_url)
    invocation["endpoint"] = base_url + selected_path

    methods = get_path_methods(spec=spec, path=selected_path)
    print("\nAvailable methods:")
    for method in methods:
        print(f"- {method}")

    selected_methods = input("\nPlease enter comma-separated methods (e.g., get,post): ").strip().lower()
    while not selected_methods:
        print("\nPlease select at least one method!")
        selected_methods = input("Please enter comma-separated methods (e.g., get,post): ").strip().lower()
    selected_methods = [m.strip() for m in selected_methods.split(",")]
    print("Selected methods: ", selected_methods)

    request_schemas, components, response_schemas = get_endpoint_schemas_and_components(
        path=selected_path, methods=selected_methods, spec=spec
    )

    preprocessing_jsonpath = input("\nEnter preprocessing jsonpath (or press Enter for empty string): ").strip()
    while preprocessing_jsonpath and (
        not is_valid_jsonpath(preprocessing_jsonpath) or not process_schema(request_schemas, preprocessing_jsonpath)
    ):
        print("\nInvalid jsonpath string!")
        preprocessing_jsonpath = input("Enter preprocessing jsonpath (or press Enter for empty string): ").strip()

    # Currently doing this here so LLM generates request with preprocessing applied (instead of generating full request and then preprocessing)
    if preprocessing_jsonpath:
        request_schemas = process_schema(request_schemas, preprocessing_jsonpath)

    postprocessing_jsonpath = input("\nEnter postprocessing jsonpath (or press Enter for empty string): ").strip()
    while not is_valid_jsonpath(postprocessing_jsonpath):
        print("\nInvalid jsonpath string!")
        postprocessing_jsonpath = input("Enter postprocessing jsonpath (or press Enter for empty string): ").strip()

    try:
        tool = ConfigBinTool(
            tool_id=tool_id,
            info=info,
            response_schema=response_schemas,
            preprocessing_jsonpath=preprocessing_jsonpath,
            postprocessing_jsonpath=postprocessing_jsonpath,
            permissions={},
            openapi=openapi,
            request_schema=request_schemas,
            invocation=invocation,
            components=components,
        )
        print("Successfully built the tool!")
        return tool
    except ValidationError as e:
        print(f"\nError creating ConfigBinTool: {e}")
        return None


if __name__ == "__main__":
    cli()
