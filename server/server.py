from typing import Any, List, Dict

from mcp.server.fastmcp import FastMCP

from csv_handler import CSVHandler

mcp = FastMCP("EDA-Assistant")

csv_handler = CSVHandler("resources/csv")

@mcp.resource("csv://available/list")
def list_available_csvs() -> List[str]:
    return csv_handler.list_dir()

@mcp.resource("csv://file/{filename}/info")
def get_file_info(filename: str) -> Dict:
    return csv_handler.get_metadata(filename)

@mcp.resource("csv://file/{filename}/schema")
def get_file_schema(filename: str) -> Dict:
    return csv_handler.get_schema(filename)

@mcp.resource("csv://file/{filename}/preview")
def get_file_preview(filename: str) -> Dict:
    return csv_handler.get_preview(filename)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()