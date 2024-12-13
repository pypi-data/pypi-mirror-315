"""
@description: CLI for chainthon
@author: rontom
@license: Apache License, Version 2.0
"""
import asyncio
import os

import click
import uvicorn

from chainthon.version import __version__
from chainthon.logger import logger


@click.group(context_settings={
    "help_option_names": ["-h", "--help"], 
    "max_content_width": 120, 
    "terminal_width": 120, 
    "show_default": True, 
    "auto_envvar_prefix": "CHAINTHON",
    "color": True, 
    "help": "A Python library for building chatbots and conversational applications", 
    "epilog": "A Python library for building chatbots and conversational applications"})
@click.version_option(version=__version__, prog_name="chainthon")
def cli():
    pass


@cli.command(help="Start the chainthon server")
@click.option("--host", default="127.0.0.1", help="Host IP address")
@click.option("--port", default=8000, help="Port number")
@click.option("--debug", default=False, is_flag=True, help="Debug mode")
async def run(host, port, debug):
    uvicorn.run("chainthon.app:app", host=host, port=port, debug=debug)


if __name__ == "__main__":
    asyncio.run(cli())