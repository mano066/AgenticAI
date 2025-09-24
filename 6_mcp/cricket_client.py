import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
from agents import FunctionTool
import json

# Replace cricket_server.py with the actual filename of your MCP server
params = StdioServerParameters(command="uv", args=["run", "cricket_server.py"], env=None)


# --- Tool listing ---
async def list_cricket_tools():
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools


# --- Tool call ---
async def call_cricket_tool(tool_name, tool_args):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result


# --- Resources (optional, if your server exposes them) ---
async def read_scoreboard_resource(match_id: str):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"cricket://scoreboard/{match_id}")
            return result.contents[0].text


async def read_batting_resource(match_id: str):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"cricket://batting/{match_id}")
            return result.contents[0].text


async def read_bowling_resource(match_id: str):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"cricket://bowling/{match_id}")
            return result.contents[0].text


# --- Expose as OpenAI-style tools ---
async def get_cricket_tools_openai():
    openai_tools = []
    for tool in await list_cricket_tools():
        schema = {**tool.inputSchema, "additionalProperties": False}
        openai_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=lambda ctx, args, toolname=tool.name: call_cricket_tool(
                toolname, json.loads(args)
            ),
        )
        openai_tools.append(openai_tool)
    return openai_tools
