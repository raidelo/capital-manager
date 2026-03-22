import typer
import uvicorn

app = typer.Typer()


@app.command()
def ping():
    """Check CLI is working"""
    print("pong")


@app.command()
def api(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
):
    """Run the FastAPI server"""
    uvicorn.run(
        "capital_manager.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
