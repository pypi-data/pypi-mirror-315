from typing import Optional, List
from typing_extensions import Annotated
from pathlib import Path
from enum import Enum

import typer
import click

from zenplate.config import Config
from zenplate.__main__ import main


cli = typer.Typer()


class LogLevels(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


@cli.command("", no_args_is_help=True)
def run(
    template: Annotated[
        Optional[Path],
        typer.Argument(
            help="The path to the jinja template / directory that zenplate will render",
            dir_okay=True,
            file_okay=True,
        ),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Argument(
            help="The path to where you'll find the output of zenplate",
            dir_okay=True,
            file_okay=True,
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path],
        typer.Option(
            help="The location of the yaml configuration file",
            show_default=True,
            dir_okay=False,
            envvar="ZENPLATE_CONFIG_FILE",
        ),
    ] = None,
    variables: Annotated[
        Optional[List[str]],
        typer.Option(
            help="A 'varname=value' pair representing a variable. May be used multiple times."
        ),
    ] = None,
    var_file: Annotated[
        Optional[List[Path]],
        typer.Option(
            help="The path to a yaml file containing key: value pairs to be used as variables. "
            "may be used multiple times.",
            dir_okay=False,
            envvar="ZENPLATE_VAR_FILE",
        ),
    ] = None,
    log_path: Annotated[
        Optional[Path],
        typer.Option(
            help="The location of the log file",
            dir_okay=False,
            envvar="ZENPLATE_LOG_PATH",
        ),
    ] = None,
    log_level: Annotated[
        Optional[LogLevels],
        typer.Option(
            help="The logging verbosity level",
            show_default=True,
            envvar="ZENPLATE_LOG_LEVEL",
        ),
    ] = LogLevels.error,
    export_config: Annotated[
        bool,
        typer.Option(
            help="When provided, the current set of configuration parameters will be exported "
            "to '--config-file' or './zenplate_config_export.yml' if not provided",
            is_flag=True,
            flag_value=True,
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            help="When provided, output will overwrite any file in that path",
            is_flag=True,
        ),
    ] = False,
    stdout: Annotated[
        bool,
        typer.Option(
            help="Write rendered template to stdout",
            is_flag=True,
        ),
    ] = False,
):
    if (not template and not output) and not export_config:
        raise click.exceptions.BadArgumentUsage(
            "You must provide both 'template' and 'output' arguments "
            "unless the '--help' or '--export-config' flags are provided."
        )
    if (template and not output) or (output and not template):
        raise click.exceptions.BadArgumentUsage(
            "You must provide both 'template' and 'output' arguments."
        )
    if (
        (template and output.exists())
        and (template and template.is_dir() and output and not output.is_dir())
        or (template and template.is_file() and output and not output.is_file())
    ):
        raise click.exceptions.BadArgumentUsage(
            "Template and output paths must both be either directories or files."
        )

    config = Config()
    if config_file:
        config.configure_from_path(config_file)
    if log_path:
        config.log_path = log_path
    if variables:
        config.variables = variables
    if var_file:
        config.var_files = [Path(i) for i in var_file]
    if template and template.is_dir():
        config.tree_directory = template
    elif template and template.is_file():
        config.template_path = template
    elif not template:
        pass
    else:
        raise click.exceptions.BadArgumentUsage(
            f"Template path '{template}' is not a file or directory."
        )
    if output:
        config.output_path = Path(output)
    if export_config:
        config.export_config()
        exit(0)

    config.force_overwrite = force
    config.stdout = stdout
    config.log_level = log_level

    main(config)


if __name__ == "__main__":
    cli()
