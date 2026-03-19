from plistlib import loads

import click
from qa4sm_api.commands import login as login_with_credentials
from qa4sm_api.commands import list_datasets, list_versions

from qa4sm_api.globals import (
    DEFAULT_INSTANCE, KNOWN_INSTANCES, QA4SM_DOTRC_PATH,
    _connect_with_credentials, _write_dotrc, _load_dotrc
)

@click.command("login")
@click.option(
    "--instance",
    default=DEFAULT_INSTANCE,
    show_default=True,
    help=(
            "QA4SM instance to log in to. "
            f"Common values: {', '.join(KNOWN_INSTANCES)}"
    ),
)
def cli_login(instance: str) -> None:
    """Authenticate with a QA4SM instance and store the token in ~/.qa4smapirc."""
    login_with_credentials(instance)


@click.command("datasets")
@click.option(
    "--instance",
    default=DEFAULT_INSTANCE,
    show_default=True,
    help=(
            "QA4SM instance to log in to. "
            f"Common values: {', '.join(KNOWN_INSTANCES)}"
    ),
)
def cli_datasets(instance):
    list_datasets(instance)




@click.command("versions")
@click.argument("dataset", type=click.STRING)
@click.option(
    "--instance",
    default=DEFAULT_INSTANCE,
    show_default=True,
    help=(
            "QA4SM instance to log in to. "
            f"Common values: {', '.join(KNOWN_INSTANCES)}"
    ),
)
def cli_versions(dataset, instance):
    list_versions(dataset, instance)


@click.group(short_help="QA4SM API access from terminal via the `qa4sm_api` "
                        "python package")
def qa4sm():
    pass

@click.group(short_help="List various information retrieved the service")
def list():
    pass

qa4sm.add_command(cli_login)
qa4sm.add_command(list)
list.add_command(cli_datasets)
list.add_command(cli_versions)


if __name__ == "__main__":
    cli_versions("test.qa4sm.eu")