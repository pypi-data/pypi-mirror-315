from setuptools import setup

setup(
    name="api-gateway",
    setup_requires="setupmeta",
    versioning="distance",
    author="copilot-platform@netflix.com",
    url="https://github.netflix.net/corp/ncp-api-gateway",
    entry_points={
        "console_scripts": [
            "run-webapp = api_gateway.webapp:main",
        ],
    },
)
