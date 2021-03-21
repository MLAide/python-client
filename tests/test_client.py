from pytest_mock.plugin import MockerFixture
import pytest

from mlaide.client import MLAideClient, ConnectionOptions


@pytest.fixture
def mock_authenticated_client(mocker: MockerFixture):
    return mocker.patch('mlaide.client.AuthenticatedClient')


@pytest.fixture
def mock_active_run(mocker: MockerFixture):
    return mocker.patch('mlaide.client.ActiveRun')


@pytest.fixture
def mock_active_artifact(mocker: MockerFixture):
    return mocker.patch('mlaide.client.ActiveArtifact')


def test_init_should_raise_value_error_if_project_key_is_none():
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        MLAideClient(None)


def test_init_should_use_default_options_if_no_options_provided(monkeypatch):
    # arrange
    monkeypatch.setenv('MLAIDE_API_KEY', 'the api key')

    # act
    client = MLAideClient('project key', options=None)

    # assert
    options = client.options
    assert options.api_key == 'the api key'
    assert options.server_url == 'http://localhost:9000/api/v1'


def test_init_should_use_merge_provided_options_with_default_options(monkeypatch):
    # arrange
    monkeypatch.setenv('MLAIDE_API_KEY', 'the api key')

    # act
    client = MLAideClient('project key', options=ConnectionOptions(server_url='http://my-server.com'))

    # assert
    options = client.options
    assert options.api_key == 'the api key'
    assert options.server_url == 'http://my-server.com'


def test_init_should_create_authenticated_client(mock_authenticated_client):
    # act
    client = MLAideClient('project key', options=ConnectionOptions(server_url='http://my-server.com', api_key='the key'))

    # assert
    mock_authenticated_client.assert_called_once_with(base_url='http://my-server.com', api_key='the key')
    assert client.api_client == mock_authenticated_client.return_value


def test_start_new_run_should_instantiate_new_active_run_with_correct_arguments(
        mock_authenticated_client, mock_active_run):
    # arrange
    client = MLAideClient('project key')
    used_artifacts = []

    # act
    active_run = client.start_new_run('experiment key', 'run name', used_artifacts)

    # assert
    mock_active_run.assert_called_once_with(
        mock_authenticated_client.return_value, 'project key', 'experiment key', 'run name', used_artifacts)
    assert active_run == mock_active_run.return_value


def test_get_artifact_should_instantiate_new_active_artifact_with_correct_arguments(
        mock_authenticated_client, mock_active_artifact):
    # arrange
    client = MLAideClient('project key')

    # act
    active_artifact = client.get_artifact('a name', 'a version')

    # assert
    mock_active_artifact.assert_called_once_with(
        mock_authenticated_client.return_value, 'project key', 'a name', 'a version')
    assert active_artifact == mock_active_artifact.return_value
