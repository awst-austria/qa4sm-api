from pathlib import Path
import os
import  warnings
import configparser

if "QA4SM_DOTRC" in os.environ:
    QA4SM_DOTRC_PATH = Path(os.environ["QA4SM_DOTRC"])
else:
    QA4SM_DOTRC_PATH = Path.home() / ".qa4smapirc"

DEFAULT_INSTANCE = "qa4sm.eu"
KNOWN_INSTANCES = ["qa4sm.eu", "test.qa4sm.eu", "test2.qa4sm.eu", "0.0.0.0:8000"]

class ValidationRunNotFoundError(ValueError):

    def __init__(self, id):
        self.message = (f"Validation run {id} not found on current "
                        f"QA4SM instance.")
        super().__init__(self.message)


class ValidationRunError(Exception):

    def __init__(self, message="Validation run failed"):
        self.message = message
        super().__init__(self.message)


class ValidationInstanceError(KeyError):

    def __init__(self, message="Unknown validation instance"):
        self.message = message
        super().__init__(self.message)

def _write_dotrc(config: dict, path=QA4SM_DOTRC_PATH):
    """
    Write credentials to a .qa4smapirc file.

    Parameters
    ----------
    config : dict
        Credentials keyed by hostname, e.g.:
        {
            "qa4sm.eu":      {"token": "...", "username": "..."},
            "test.qa4sm.eu": {"token": "..."},
        }
    path : str or Path, optional
        Path to the .qa4smapirc file
    """

    with open(path, 'w') as f:
        for host, fields in config.items():
            f.write(f'[{host}]\n')
            for key, value in fields.items():
                f.write(f'{key}: {value}\n')
            f.write('\n')


def _load_dotrc(path=QA4SM_DOTRC_PATH):
    """
    Read credentials from a .qa4smapirc file.

    Parameters
    ----------
    path : str or Path, optional
        Path to the .qa4smapirc file

    Returns
    -------
    config : dict
        Credentials keyed by hostname, e.g.:
        {
            "qa4sm.eu":      {"token": "..."},
            "test.qa4sm.eu": {"token": "..."},
        }
        Sections named 'default' or 'qa4sm' both map to 'qa4sm.eu'.
        All other section names (e.g. 'test', 'test2') map to '<name>.qa4sm.eu'.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f'QA4SM credentials file not found at {path}. '
            f'Please check https://qa4sm.eu/ui/public-api'
        )

    PRODUCTION_SECTIONS = {"default", "qa4sm", "qa4sm.eu"}

    def section_to_host(section: str) -> str:
        return "qa4sm.eu" if section.lower() in PRODUCTION_SECTIONS \
            else section

    parser = configparser.ConfigParser()
    parser.read(path)

    config = {}

    # Handle DEFAULT first — named sections will override it if they resolve
    # to the same host (e.g. [qa4sm] overrides [DEFAULT] for 'qa4sm.eu')
    if parser.defaults():
        config[section_to_host("default")] = dict(parser.defaults())

    for section in parser.sections():
        config[section_to_host(section)] = dict(parser[section])

    return config


def _connect_with_credentials(instance: str, username: str, password: str) -> dict:
    """
    Open a Session to the given instance, authenticate with username/password,
    and return the auth token.
    """
    # Import here so the CLI works even if the rest of the package isn't
    # fully installed — errors surface only when login is actually attempted.
    from qa4sm_api.client_api import Session

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        session = Session(instance=instance, token="none")
        session.login_with_credentials(username=username, password=password)
        access = session.access.access
    return access