"""Main FastAPI application."""
from fastapi import FastAPI
from .version import __version__

app = FastAPI(
    title="Chainthon",
    description="A Python library for building chatbots and conversational applications",
    version=__version__,
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Chainthon!"}
