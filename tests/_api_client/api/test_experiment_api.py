from pytest_mock.plugin import MockerFixture
import pytest

import mlaide._api_client.api.experiment_api as experiment_api
from mlaide._api_client.dto import ExperimentDto


@pytest.fixture
def client(mocker: MockerFixture):
    client = mocker.patch('mlaide._api_client.api.experiment_api.Client')()
    client.base_url = 'https://mlaide.com'
    client.get_headers.return_value = {'x-api-key': 'xyz'}
    return client


@pytest.fixture
def assert_response_status_mock(mocker: MockerFixture):
    return mocker.patch('mlaide._api_client.api.experiment_api.assert_response_status')


def test_create_experiment_should_return_created_experiment(client, httpx_mock):
    # arrange
    experiment = ExperimentDto(key='exp key')
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/experiments',
                            match_headers=client.get_headers(),
                            match_content=b'{"key": "exp key"}',
                            json={'key': 'saved'},
                            status_code=200)

    # act
    created_experiment = experiment_api.create_experiment(client=client, project_key='pk', experiment=experiment)

    # assert
    assert httpx_mock.get_request() is not None
    assert created_experiment is not None
    assert created_experiment.key == 'saved'


def test_create_experiment_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    experiment = ExperimentDto(key='exp key')
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/experiments',
                            match_headers=client.get_headers(),
                            match_content=b'{"key": "exp key"}',
                            json={'code': 500, 'message': 'error'},
                            status_code=500)

    # act
    experiment_api.create_experiment(client=client, project_key='pk', experiment=experiment)

    # assert
    assert httpx_mock.get_request() is not None
    assert_response_status_mock.assert_called_once()


def test_get_experiment_should_return_experiment(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/experiments/e',
                            match_headers=client.get_headers(),
                            status_code=200,
                            json={'key': 'experiment key'})

    # act
    experiment = experiment_api.get_experiment(client=client, project_key='pk', experiment_key='e')

    # assert
    assert httpx_mock.get_request() is not None
    assert experiment.key == 'experiment key'


def test_get_experiment_return_404_should_return_none(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/experiments/e',
                            match_headers=client.get_headers(),
                            status_code=404)

    # act
    experiment = experiment_api.get_experiment(client=client, project_key='pk', experiment_key='e')

    # assert
    assert httpx_mock.get_request() is not None
    assert experiment is None


def test_get_experiment_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/experiments/e',
                            match_headers=client.get_headers(),
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    # act
    experiment_api.get_experiment(client=client, project_key='pk', experiment_key='e')

    # assert
    assert_response_status_mock.assert_called_once()
