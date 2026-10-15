from mcp.server.fastmcp import FastMCP
import logging
from pathlib import Path

# Configure logging to only show errors
logging.basicConfig(level=logging.ERROR)

# Initialize FastMCP server for saving reports
mcp = FastMCP("save-report")

# Reports are confined to <project>/reports/ regardless of the server's working directory
REPORTS_DIR = (Path(__file__).resolve().parent.parent / "reports")

@mcp.tool()
async def save_report(report: str, file_name: str="report.md") -> None:
    """
    Save the generated financial report to a file

    Args:
        report (str): The report content to be saved
        file_name (str): The filename to save the report to. Defaults to "report.md"
    """
    # Append the report content to the specified file inside reports/
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    target = (REPORTS_DIR / Path(file_name).name).resolve()
    if not target.is_relative_to(REPORTS_DIR) or target.suffix.lower() not in {".md", ".txt"}:
        raise ValueError(f"Refusing to write report to {file_name!r}")
    with open(target, "a") as file:
        file.write(report + "\n")
    print("Report saved successfully!")

def run_save_report_server():
    """Start the report saving MCP server using stdio transport"""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run_save_report_server()
