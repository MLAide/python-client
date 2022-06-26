from pytest_mock.plugin import MockerFixture
import pytest

from mlaide import MLAideClient, ConnectionOptions, ModelStage


@pytest.fixture
def mock_authenticated_client(mocker: MockerFixture):
    return mocker.patch('mlaide.client.AuthenticatedClient')


@pytest.fixture
def mock_active_run(mocker: MockerFixture):
    return mocker.patch('mlaide.client.ActiveRun')


@pytest.fixture
def mock_active_artifact(mocker: MockerFixture):
    return mocker.patch('mlaide.client.ActiveArtifact')


@pytest.fixture
def mock_get_git_metadata(mocker: MockerFixture):
    return mocker.patch('mlaide.client.get_git_metadata')


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


def test_get_artifact_should_instantiate_new_active_artifact_with_correct_arguments(
        mock_authenticated_client, mock_active_artifact):
    # arrange
    client = MLAideClient('project key')

    # act
    active_artifact = client.get_artifact('a name', 5)

    # assert
    mock_active_artifact.assert_called_once_with(
        mock_authenticated_client.return_value, 'project key', 'a name', 5)
    assert active_artifact == mock_active_artifact.return_value


def test_load_model_should_instantiate_new_active_artifact_with_correct_arguments_and_return_result_of_load_model(
        mock_authenticated_client, mock_active_artifact):
    # arrange
    client = MLAideClient('project key')
    mock_active_artifact.return_value.load_model.return_value = "the deserialized model"

    # act
    model = client.load_model('model name', 7)

    # assert
    mock_active_artifact.assert_called_once_with(
        mock_authenticated_client.return_value, 'project key', 'model name', 7, None)
    assert model == "the deserialized model"


def test_load_model_should_pass_stage_to_active_artifact(mock_authenticated_client, mock_active_artifact):
    # arrange
    client = MLAideClient('project key')

    # act
    client.load_model('model name', stage=ModelStage.PRODUCTION)

    # assert
    mock_active_artifact.assert_called_once_with(
        mock_authenticated_client.return_value, 'project key', 'model name', None, ModelStage.PRODUCTION)


def test_load_model_should_raise_error_when_version_and_stage_are_defined():
    # arrange
    client = MLAideClient('project key')

    # act
    with pytest.raises(ValueError):
        client.load_model('model name', version=3, stage=ModelStage.PRODUCTION)
