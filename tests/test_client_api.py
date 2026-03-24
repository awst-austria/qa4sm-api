import tempfile
import unittest
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, MagicMock, patch
import requests
from qa4sm_api.client_api import Connection, Session, Response, ValidationConfiguration, ValidationInstanceError
from qa4sm_api.globals import ValidationRunNotFoundError
from qa4sm_api.client_api import Access

try:
    QA4SM_ACCESS = Access.from_available().access
except:
    QA4SM_ACCESS = None

class TestResponse(unittest.TestCase):
    re = [{'username': 'testuser', 'email': 'test.user@test.com',
           'first_name': 'Test', 'last_name': 'User',
           'organisation': 'asd', 'last_login': '2026-03-10T17:28:22.995415Z',
           'date_joined': '2020-07-17T13:11:25Z',
           'country': 'AT', 'orcid': '', 'id': 999, 'copied_runs': [],
           'space_limit': 'unlimited', 'space_limit_value': None,
           'space_left': None, 'is_staff': True, 'is_superuser': True,
           'auth_token': 'ab123'}]

    def setUp(self):
        self.re = Response(self.re, serialize=False)

    def test_data(self):
        data = self.re.data
        assert len(data) == 1
        data = data[0]
        assert data['space_left'] is None
        assert data['username'] == 'testuser'
        assert data['is_staff'] == True

    def test_pandas(self):
        data = self.re.pandas
        assert data['space_left'] is None
        assert data['username'] == 'testuser'
        assert data['is_staff'] == True


class TestSession(unittest.TestCase):

    def setUp(self) -> None:
        self.session = Session(instance="test.qa4sm.eu", token="none")

    def test_url_pretty(self):
        url = self.session.url("asd", "jkl/")
        assert url == "https://test.qa4sm.eu/api/asd/jkl"

    @pytest.mark.skipif(QA4SM_ACCESS is None, reason="No credentials found.")
    def test_login(self):
        token = QA4SM_ACCESS[self.session.instance]['token']
        status_code = self.session.login_with_token(token)
        assert status_code == 200


class TestValidationConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = ValidationConfiguration.from_remote(
            "9aeb663b-e24e-4541-8331-6ec3e0318d1f",
            instance="qa4sm.eu", token="none")

    def test_data_access(self):
        assert self.config['name_tag'] == "Test Case  QA4SM_VA_metrics - Test scaling_no_scaling_DEFAULT"
        assert self.config['interval_to'] == "2024-12-31"
        assert self.config['max_lon'] == 48.3
        assert self.config['min_lat'] == self.config.data['min_lat']

    def test_dump_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            self.config.dump(tmpdir / "config.json")
            also_config = ValidationConfiguration.from_file(
                tmpdir / "config.json")
            assert self.config == also_config


class TestConnectionTestInstance(unittest.TestCase):

    def setUp(self):
        self.con = Connection(instance="test.qa4sm.eu", token="None")

    def test_token_is_None(self):
        assert self.con.session.user is None

    def test_get_datasets(self):
        ds = self.con.datasets()
        assert ds.loc[1, "short_name"] == 'C3S_combined'
        assert ds.columns.size > 2

    def test_get_dataset_id(self):
        id = self.con.dataset_id("C3S_combined")
        assert id == 1

    def test_get_versions(self):
        vers = self.con.versions("C3S_combined")
        alsovers = self.con.versions(1)
        assert vers.equals(alsovers)

    def test_get_version_info(self):
        vers = self.con.version_info(70)
        assert vers["short_name"] == "C3S_V202505"
        assert vers["id"] == 70

    def test_get_variable_info(self):
        id = 1
        var = self.con.variable_info(id)
        assert var["short_name"] == "sm"
        assert var["id"] == id

    def test_get_filter_info(self):
        id = 1
        fil = self.con.filter_info(id)
        assert fil["name"] == "FIL_ALL_VALID_RANGE"
        assert fil["parameterised"] == False
        assert fil["id"] == id

    def test_get_param_filter_info(self):
        id = 18
        fil = self.con.filter_info(id)
        assert fil["name"] == "FIL_ISMN_NETWORKS"
        assert fil["parameterised"] == True
        assert fil["id"] == id

    def test_get_period(self):
        start, end = self.con.get_period(70)
        assert pd.to_datetime(start) < pd.to_datetime(end)


@pytest.mark.skipif(QA4SM_ACCESS is None, reason="No Access credentials available.")
class TestConnectionWithToken(unittest.TestCase):

    def setUp(self):
        instance = "test.qa4sm.eu"
        token = QA4SM_ACCESS[instance]['token']
        self.con = Connection(instance=instance, token=token)

    def test_url(self):
        assert (self.con.url("asd", "jkl/") ==
                "https://test.qa4sm.eu/api/asd/jkl")

    def test_user(self):
        user = self.con.user()
        assert user['auth_token'] == QA4SM_ACCESS[self.con.session.instance]['token']
        assert user['username'] == self.con.session.user


class TestValidationMonitoring(unittest.TestCase):

    def setUp(self):
        self.con = Connection(instance="test.qa4sm.eu", token="None")
        self.run_id = "9aeb663b-e24e-4541-8331-6ec3e0318d1f"

    def test_validation_status_done_state(self):
        """Test validation status for DONE state"""
        with patch.object(self.con.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.data = [{'status': 'DONE', 'progress': 100}]
            self.con.session.get = lambda url, headers=None: mock_response
            
            status, progress = self.con.validation_status(self.run_id)
            assert status == 'DONE'
            assert progress == 100

    def test_validation_status_running_state(self):
        """Test validation status for RUNNING state"""
        with patch.object(self.con.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.data = [{'status': 'RUNNING', 'progress': 50}]
            self.con.session.get = lambda url, headers=None: mock_response
            
            status, progress = self.con.validation_status(self.run_id)
            assert status == 'RUNNING'
            assert progress == 50

    def test_validation_status_not_found(self):
        """Test validation status when run doesn't exist"""
        from tornado.httpclient import HTTPError
        with patch.object(self.con.session, 'get') as mock_get:
            mock_get.side_effect = HTTPError(code=404)
            
            status, progress = self.con.validation_status(self.run_id)
            assert status == 'NOT FOUND'
            assert progress == 0

    def test_validation_time(self):
        """Test validation timing retrieval"""
        with patch.object(self.con.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.data = [{
                'start_time': '2024-03-24T10:00:00Z',
                'end_time': '2024-03-24T10:30:00Z'
            }]
            self.con.session.get = lambda url, headers=None: mock_response
            
            start_time, end_time = self.con.validation_time(self.run_id)
            assert start_time is not None
            assert end_time is not None
            assert end_time > start_time

    def test_validation_duration(self):
        """Test validation duration calculation"""
        with patch.object(self.con.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.data = [{
                'duration_seconds': 3600,
                'duration_format': '1h 0m 0s'
            }]
            self.con.session.get = lambda url, headers=None: mock_response
            
            seconds, formatted = self.con.validation_duration(self.run_id)
            assert seconds == 3600
            assert formatted == '1h 0m 0s'


class TestDownloadFunctionality(unittest.TestCase):

    def setUp(self):
        self.con = Connection(instance="test.qa4sm.eu", token="None")
        self.run_id = "9aeb663b-e24e-4541-8331-6ec3e0318d1f"
        self.test_config = {
            'name_tag': 'test',
            'interval_from': '2024-01-01',
            'interval_to': '2024-12-31'
        }

    def test_download_configuration(self):
        """Test downloading and saving validation configuration"""
        with patch.object(self.con.session, 'get') as mock_get:
            mock_response = Mock()
            mock_response.data = [self.test_config.copy()]
            self.con.session.get = lambda url, headers=None: mock_response
            
            config = self.con.download_configuration(self.run_id)
            assert config['name_tag'] == 'test'
            assert config['interval_from'] == '2024-01-01'


class TestErrorCases(unittest.TestCase):

    def setUp(self):
        self.con = Connection(instance="test.qa4sm.eu", token="None")
        self.run_id = "9aeb663b-e24e-4541-8331-6ec3e0318d1f"

    @patch('qa4sm_api.client_api.Connection.validation_exists', return_value=False)
    def test_validation_not_found_error(self, mock_exists):
        """Test ValidationRunNotFoundError is raised for invalid run ID"""
        with self.assertRaises(ValidationRunNotFoundError):
            self.con.validation_time(self.run_id)


def test_unknown_instance():
    with pytest.warns(UserWarning):
        conn = Connection("unknown_instance.com", token="none")
    with pytest.raises(requests.exceptions.ConnectionError):
        conn.datasets()

if __name__ == '__main__':
    test_unknown_instance()
    #connection = TestConnectionWithToken()
    #connection.setUp()
    #connection.test_url()
