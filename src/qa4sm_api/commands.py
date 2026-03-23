import os
import click
import pandas as pd

from qa4sm_api.globals import (_connect_with_credentials,
                               QA4SM_DOTRC_PATH, _load_dotrc, _write_dotrc,
                               DEFAULT_INSTANCE)
from qa4sm_api.client_api import Connection




def list_datasets(instance=DEFAULT_INSTANCE):
    """
    Print a table of all datasets available on the instance.
    """
    qa4sm = Connection(instance)
    table = qa4sm.datasets()[['short_name', 'pretty_name', 'user']]
    table['user'] = table['user'].fillna('Public')
    table = table.rename(columns={'short_name': 'Name',
                                     'pretty_name': 'Long Name',
                                     'user': 'Owner'})

    with pd.option_context(
            'display.max_rows', None,
            'display.max_colwidth', 50, 'display.width', 120):
        print(table.to_string())


def list_versions(dataset, instance=DEFAULT_INSTANCE):
    """
    List the available versions for a dataset.
    """
    qa4sm = Connection(instance)
    table = qa4sm.versions(dataset)
    with pd.option_context(
            'display.max_rows', None,
            'display.max_colwidth', 50, 'display.width', 120):
        print(table.to_string())

def list_variables(datset, version, instance=DEFAULT_INSTANCE):
    qa4sm = Connection(instance)
    qa4sm.dataset_info()


if __name__ == '__main__':
    list_datasets("test.qa4sm.eu")
    list_versions('C3S_combined', "test.qa4sm.eu")