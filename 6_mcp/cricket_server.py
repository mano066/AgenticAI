# mcp_server_cricket.py
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

API_KEY = "7a943fe5-6e5a-46c4-b610-d9b72d8fd7ee"  # get one from https://www.cricapi.com/
BASE_URL = "https://api.cricapi.com/v1"

mcp = FastMCP("cricket_server")

async def fetch_api(endpoint: str, params: dict = None):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/{endpoint}", params={"apikey": API_KEY, **(params or {})})
        resp.raise_for_status()
        return resp.json()

# --- Tools ---

@mcp.tool()
async def get_live_score(match_id: str) -> str:
    """Get the live score summary for a given match ID."""
    data = await fetch_api("currentMatches")
    for match in data.get("data", []):
        if match.get("id") == match_id:
            return f"{match['name']} - {match['status']}"
    return "Match not found or not live."

@mcp.tool()
async def get_batting(match_id: str) -> list[dict]:
    """Get the current batting players for a given match."""
    data = await fetch_api("currentMatches")
    for match in data.get("data", []):
        if match.get("id") == match_id and "score" in match:
            batting = []
            for s in match["score"]:
                if s.get("inning").lower().startswith("batting"):
                    batting.append(s)
            return batting
    return []

@mcp.tool()
async def get_bowling(match_id: str) -> list[dict]:
    """Get the current bowling players for a given match."""
    data = await fetch_api("currentMatches")
    for match in data.get("data", []):
        if match.get("id") == match_id and "score" in match:
            bowling = []
            for s in match["score"]:
                if s.get("inning").lower().startswith("bowling"):
                    bowling.append(s)
            return bowling
    return []

@mcp.tool()
async def get_scoreboard(match_id: str) -> dict:
    """Get the full scoreboard for a given match."""
    return await fetch_api("match_scorecard", {"id": match_id})

# --- Resources ---

@mcp.resource("cricket://score/{match_id}")
async def read_score_resource(match_id: str) -> str:
    return await get_live_score(match_id)

@mcp.resource("cricket://scoreboard/{match_id}")
async def read_scoreboard_resource(match_id: str) -> dict:
    return await get_scoreboard(match_id)

# --- Run Server ---

if __name__ == "__main__":
    mcp.run(transport="stdio")
