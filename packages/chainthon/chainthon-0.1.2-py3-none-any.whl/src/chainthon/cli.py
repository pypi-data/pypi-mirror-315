"""
@description: CLI for chainthon
@author: rontom
@license: Apache License, Version 2.0
"""
import asyncio

import click
import uvicorn
from click import Context

from chainthon.utils.nest_event import apply

apply()

from chainthon.version import __version__
from chainthon.logger import logger


class AsyncCLI(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._async_func = None

    def command(self, *args, **kwargs):
        decorator = super().command(*args, **kwargs)
        if kwargs.get('async_command', False):
            def wrapper(f):
                self._async_func = f
                return decorator(f)
            return wrapper
        return decorator

    def invoke(self, ctx: Context):
        if self._async_func is not None:
            # 如果是异步函数，使用 asyncio 运行
            asyncio.run(self._async_func(**ctx.params))
        else:
            # 否则正常调用
            super().invoke(ctx)


@click.group(
    cls=AsyncCLI,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": 120,
        "terminal_width": 120,
        "show_default": True,
        "auto_envvar_prefix": "CHAINTHON",
        "color": True
    },
    help="A Python library for building chatbots and conversational applications",
    epilog="A Python library for building chatbots and conversational applications"
)
@click.version_option(version=__version__, prog_name="chainthon")
def cli():
    """Chainthon CLI tool"""
    pass


@cli.command(
    help="Start the chainthon server",
    short_help="Start server"
)
@click.option(
    "--host",
    default="127.0.0.1",
    help="Host IP address",
    show_default=True
)
@click.option(
    "--port",
    default=8000,
    help="Port number",
    type=int,
    show_default=True
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug mode",
    show_default=True
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    help="Enable auto-reload",
    show_default=True
)
def run(
    host: str,
    port: int,
    debug: bool,
    reload: bool
):
    """Start the Chainthon server"""
    try:
        logger.info(f"Starting server at http://{host}:{port}")
        uvicorn.run(
            "chainthon.app:app",
            host=host,
            port=port,
            debug=debug,
            reload=reload,
            log_level="debug" if debug else "info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise click.ClickException(str(e))


@cli.command(
    help="Initialize a new Chainthon project",
    short_help="Create new project"
)
@click.argument(
    "project_name",
    type=str,
    required=True
)
@click.option(
    "--template",
    default="basic",
    help="Project template to use",
    type=click.Choice(["basic", "advanced"]),
    show_default=True
)
def init(project_name: str, template: str):
    """Initialize a new Chainthon project"""
    try:
        # 项目初始化逻辑
        logger.info(f"Creating new project: {project_name}")
        # ...
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise click.ClickException(str(e))


def main():
    """Entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        logger.error(f"CLI error: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
