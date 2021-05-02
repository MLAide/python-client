from pytest_mock.plugin import MockerFixture
import pytest

import mlaide._api_client.api.run_api as run_api


@pytest.fixture
def client(mocker: MockerFixture):
    client = mocker.patch('mlaide._api_client.api.run_api.Client')()
    client.base_url = 'https://mlaide.com'
    client.get_headers.return_value = {'x-api-key': 'xyz'}
    return client


@pytest.fixture
def assert_response_status_mock(mocker: MockerFixture):
    return mocker.patch('mlaide._api_client.api.run_api.assert_response_status')


def test_create_run_should_create_and_return_new_run(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/project key/runs',
                            match_headers=client.get_headers(),
                            match_content=b'{"name": "run name"}',
                            json={'name': 'saved'})

    run = run_api.RunDto(name='run name')

    # act
    saved_run = run_api.create_run(client=client, project_key='project key', run=run)

    # assert
    assert saved_run.name == 'saved'
    assert httpx_mock.get_request() is not None


def test_create_run_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/project key/runs',
                            match_headers=client.get_headers(),
                            match_content=b'{"name": "run name"}',
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    run = run_api.RunDto(name='run name')

    # act
    run_api.create_run(client=client, project_key='project key', run=run)

    # assert
    assert_response_status_mock.assert_called_once()


def test_partial_update_run_should_update_run(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"name": "run name"}',
                            status_code=204)

    run = run_api.RunDto(name='run name')

    # act
    run_api.partial_update_run(client=client, project_key='project key', run_key=38, run=run)

    # assert
    assert httpx_mock.get_request() is not None


def test_partial_update_run_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"name": "run name"}',
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    run = run_api.RunDto(name='run name')

    # act
    run_api.partial_update_run(client=client, project_key='project key', run_key=38, run=run)

    # assert
    assert_response_status_mock.assert_called_once()


def test_update_run_parameters_should_update_run_parameters(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38/parameters',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"foo": "bar"}',
                            status_code=204)

    parameters = {'foo': 'bar'}

    # act
    run_api.update_run_parameters(client=client, project_key='project key', run_key=38, parameters=parameters)

    # assert
    assert httpx_mock.get_request() is not None


def test_update_run_parameters_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38/parameters',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"foo": "bar"}',
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    parameters = {'foo': 'bar'}

    # act
    run_api.update_run_parameters(client=client, project_key='project key', run_key=38, parameters=parameters)

    # assert
    assert_response_status_mock.assert_called_once()


def test_update_run_metrics_should_update_run_metrics(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38/metrics',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"foo": "bar"}',
                            status_code=204)

    metrics = {'foo': 'bar'}

    # act
    run_api.update_run_metrics(client=client, project_key='project key', run_key=38, metrics=metrics)

    # assert
    assert httpx_mock.get_request() is not None


def test_update_run_metrics_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='PATCH',
                            url='https://mlaide.com/projects/project key/runs/38/metrics',
                            match_headers={'x-api-key': 'xyz', 'content-type': 'application/merge-patch+json'},
                            match_content=b'{"foo": "bar"}',
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    metrics = {'foo': 'bar'}

    # act
    run_api.update_run_metrics(client=client, project_key='project key', run_key=38, metrics=metrics)

    # assert
    assert_response_status_mock.assert_called_once()
