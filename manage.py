"""
Runs the application for local development or production.
"""
import os
import sys

import uvicorn
from rich.console import Console
def run_server(environment):
    import uvicorn
    os.environ["APP_ENV"] = environment
    host = "127.0.0.1"
    port = 8000
    workers = 1 if environment == "dev" else 10

    console = Console()
    console.rule(f"[bold red] Running in {environment} environment", align="left")

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info",
        reload=True if environment == "dev" else False,
        server_header=False,
    )


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["dev", "prod"]:
        print("Usage: python manage.py [dev|prod]")
        sys.exit(1)

    command = sys.argv[1]
    run_server(command)