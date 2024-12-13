from textwrap import dedent

import logging
import json
from enum import Enum
from typing import Any, List
import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pathlib import Path

from pydantic.networks import AnyUrl
from . import explorer

server = Server(
    "mcp-server-docs",
)

async def serve(repositories: dict[str, str]) -> None:
    logger = logging.getLogger(__name__)

    # Create DocumentExplorer instance
    doc_explorer = explorer.DocumentationFileExplorer(
        root_paths=repositories
    )
    await doc_explorer.crawl_documents()

    # Dynamically create enum from document keys
    VALID_DOCUMENT_PATHS = list(doc_explorer.documents.keys())
    VALID_REPOSITORIES = list(doc_explorer.root_paths.keys())


    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        """List all available documentation resources."""
        resources = []
        for document_key, doc in sorted(doc_explorer.documents.items(), key=lambda x: x[1].title):
            resources.append(
                types.Resource(
                    uri=AnyUrl(f"file://{document_key.repository}/{document_key.path}"),
                    name=f"[{doc.repository}][{document_key.path}] {doc.title}",
                    description=f"({doc.repository}): {doc.description}",
                    mimeType="text/markdown"
                )
            )
        return resources

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        """Read content from a documentation resource."""
        # Extract path from URI
        uri_str = str(uri)
        if not uri_str.startswith("file://"):
            raise ValueError(f"Invalid URI scheme: {uri}")

        full_path = uri_str[7:].split('/', maxsplit=1)  # Remove "file://" prefix
        repository, path = full_path[0], full_path[1]
        if doc := doc_explorer.get(repository=repository, path=path):
            content = f"# {doc.title}\n\n"
            if doc.description:
                content += f"{doc.description}\n\n"
            content += doc.content

            return content
        else:
            raise ValueError(f"Document not found: ({json.dumps(full_path)}) {sorted(doc_explorer.documents.items(), key=lambda x: x[1].title)}")


    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        List available tools.
        The fetch-documents tool allows retrieving content from pre-crawled documentation.
        """
        return [
            types.Tool(
                name="fetch-documents",
                description=dedent("""Use this tool to retrieve relevant technical documentation files.
                            This tool can help find and fetch documentation across multiple repositories and topics.

                            The tool will:
                            - Search through available documentation files
                            - Return relevant content based on the repository and path specified
                            - Provide structured documentation with headers, code examples, and explanations

                            Common use cases:
                            - Finding API documentation
                            - Retrieving usage guides and tutorials
                            - Looking up technical specifications
                            - Accessing implementation examples

                            Examples:
                            1. Fetch API documentation:
                                {
                                    "documents": [
                                    {
                                        "repository": "Anthropic documentation",
                                        "path": "docs/api/messages/messages"
                                    }
                                    ]
                                }

                            2. Get both overview and specific feature docs:
                                {
                                    "documents": [
                                    {
                                        "repository": "Model Context Protocol",
                                        "path": "docs/concepts/overview"
                                    },
                                    {
                                        "repository": "Model Context Protocol",
                                        "path": "docs/concepts/tools"
                                    }
                                    ]
                                }

                            3. Compare implementation approaches:
                                {
                                    "documents": [
                                    {
                                        "repository": "Python SDK",
                                        "path": "docs/implementation/basic-server"
                                    },
                                    {
                                        "repository": "TypeScript SDK",
                                        "path": "docs/implementation/basic-server"
                                    }
                                    ]
                                }
                            """.strip()),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "documents": {
                            "type": "array",
                            "description": dedent("""A list of document objects to fetch.
                                            Each document object must specify:
                                            - repository: The documentation repository/category to search in
                                            - path: The specific document path within that repository

                                            Multiple documents can be requested at once to gather related information.

                                            Examples:
                                            1. Single document:
                                                {
                                                    "documents": [
                                                    {
                                                        "repository": "Anthropic documentation",
                                                        "path": "docs/getting-started"
                                                    }
                                                    ]
                                                }

                                            2. Multiple related documents:
                                                {
                                                    "documents": [
                                                    {
                                                        "repository": "Model Context Protocol",
                                                        "path": "docs/concepts/resources"
                                                    },
                                                    {
                                                        "repository": "Model Context Protocol",
                                                        "path": "docs/concepts/tools"
                                                    }
                                                    ]
                                                }

                                            Available repositories: {VALID_REPOSITORIES}
                                            """.strip()),
                            "items": {
                                "type": "object",
                                "properties": {
                                    "repository": {
                                        "description": dedent("""Name of the documentation repository/category

                                                        Examples:
                                                        - "anthropic-documentation"
                                                        - "mcp"
                                                        - "anthropic-sdk-python"
                                                        - "anthropic-sdk-typescript"
                                                        """.strip()),
                                        "type": "string",
                                        "enum": VALID_REPOSITORIES,
                                    },
                                    "path": {
                                        "description": dedent("""Path to the specific document within the repository

                                                        Examples:
                                                        - "docs/getting-started"
                                                        - "docs/api/messages/messages"
                                                        - "docs/concepts/tools"
                                                        - "docs/implementation/basic-server"

                                                        Common path patterns:
                                                        - docs/concepts/... - Conceptual documentation
                                                        - docs/api/... - API reference
                                                        - docs/guides/... - Tutorial guides
                                                        - docs/implementation/... - Implementation details
                                                        """),
                                        "type": "string",
                                        "enum": VALID_DOCUMENT_PATHS,
                                    }
                                }
                            },
                            "minItems": 1
                        }
                    },
                    "required": ["paths"]
                }
            )
        ]


    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Handle tool execution requests.
        """
        if not arguments:
            raise ValueError("Missing arguments")

        if name == "fetch-documents":
            documents = arguments.get("documents")
            if not documents:
                return [types.TextContent(
                    type="text",
                    text="Error: Missing paths parameter"
                )]

            results = []
            for doc_obj in documents:
                if (repository := doc_obj.get("repository")) and (doc_path := doc_obj.get("path")):
                    if doc := doc_explorer.get(repository, doc_path):
                        content = f"# {doc.title}\n\n"
                        if doc.description:
                            content += f"{doc.description}\n\n"
                        content += doc.content
                        results.append(content)
                else:
                    results.append(f"Document not found: {json.dumps(doc_obj, indent=2)}")

            return [
                types.TextContent(
                    type="text",
                    text="\n\n---\n\n".join(results)
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
