from pytest_mock.plugin import MockerFixture
from io import BytesIO
import pytest

import mlaide._api_client.api.artifact_api as artifact_api


@pytest.fixture
def client(mocker: MockerFixture):
    client = mocker.patch('mlaide._api_client.api.artifact_api.Client')()
    client.base_url = 'https://mlaide.com'
    client.get_headers.return_value = {'x-api-key': 'xyz'}
    return client


@pytest.fixture
def assert_response_status_mock(mocker: MockerFixture):
    return mocker.patch('mlaide._api_client.api.artifact_api.assert_response_status')


def test_create_model_should_create_new_model(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='PUT',
                            url='https://mlaide.com/projects/pk/artifacts/my-artifact/12/model',
                            match_headers=client.get_headers(),
                            match_content=None,
                            status_code=204)

    # act
    artifact_api.create_model(client=client, project_key='pk', artifact_name='my-artifact', artifact_version=12)

    # assert
    assert httpx_mock.get_request() is not None


def test_create_model_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='PUT',
                            url='https://mlaide.com/projects/pk/artifacts/my-artifact/12/model',
                            match_headers=client.get_headers(),
                            match_content=None,
                            status_code=204)

    # act
    artifact_api.create_model(client=client, project_key='pk', artifact_name='my-artifact', artifact_version=12)

    # assert
    assert_response_status_mock.assert_called_once()


def test_create_artifact_should_create_new_artifact(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/artifacts',
                            match_headers=client.get_headers(),
                            match_content=b'{"name": "artifact name"}',
                            json={'name': 'saved'})
    artifact = artifact_api.ArtifactDto(name='artifact name')

    # act
    created_artifact = artifact_api.create_artifact(client=client, project_key='pk', artifact=artifact)

    # assert
    assert httpx_mock.get_request() is not None
    assert created_artifact.name == 'saved'


def test_create_artifact_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/artifacts',
                            match_headers=client.get_headers(),
                            match_content=b'{"name": "artifact name"}',
                            status_code=500,
                            json={'code': 500, 'message': 'error'})
    artifact = artifact_api.ArtifactDto(name='artifact name')

    # act
    artifact_api.create_artifact(client=client, project_key='pk', artifact=artifact)

    # assert
    assert_response_status_mock.assert_called_once()


def test_upload_file_should_upload_the_file(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/artifacts/artifact name/28/files?file-hash=111',
                            match_headers=client.get_headers(),
                            status_code=204)
    file = BytesIO(bytes('foobar', 'utf-8'))

    # act
    artifact_api.upload_file(client=client, 
                             project_key='pk',
                             artifact_name='artifact name',
                             artifact_version=28,
                             filename='my-file.txt',
                             file_hash='111',
                             file=file)

    # assert
    request = httpx_mock.get_request()
    assert request is not None
    body = request.read().decode('utf-8')
    assert body.find('Content-Disposition: form-data; name="file"; filename="my-file.txt"') != -1
    assert body.find('foobar') != -1


def test_upload_file_should_assert_status_code500(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='POST',
                            url='https://mlaide.com/projects/pk/artifacts/artifact name/28/files?file-hash=123',
                            match_headers=client.get_headers(),
                            status_code=500,
                            json={'code': 500, 'message': 'error'})
    file = BytesIO(bytes('foobar', 'utf-8'))

    # act
    artifact_api.upload_file(client=client,
                             project_key='pk',
                             artifact_name='artifact name',
                             artifact_version=28,
                             filename='my-file.txt',
                             file_hash='123',
                             file=file)

    # assert
    assert_response_status_mock.assert_called_once()


def test_get_artifact_should_return_artifact(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/artifacts/a/12',
                            match_headers=client.get_headers(),
                            status_code=200,
                            json={'name': 'artifact name'})

    # act
    artifact = artifact_api.get_artifact(client=client, project_key='pk', artifact_name='a', artifact_version=12)

    # assert
    assert httpx_mock.get_request() is not None
    assert artifact.name == 'artifact name'


def test_get_artifact_should_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/artifacts/a/12',
                            match_headers=client.get_headers(),
                            status_code=500,
                            json={'code': 500, 'message': 'error'})

    # act
    artifact_api.get_artifact(client=client, project_key='pk', artifact_name='a', artifact_version=12)

    # assert
    assert_response_status_mock.assert_called_once()


def test_download_artifact_should_return_artifact_bytes(client, httpx_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/artifacts/a/12/files',
                            match_headers={'x-api-key': 'xyz', 'Accepts': 'application/zip'},
                            status_code=200,
                            headers={'Content-Disposition': 'attachment; filename="artifact-12.zip"'},
                            data=b'file content')

    # act
    file, filename = \
        artifact_api.download_artifact(client=client, project_key='pk', artifact_name='a', artifact_version=12)

    # assert
    assert httpx_mock.get_request() is not None
    assert filename == 'artifact-12.zip'
    assert file.read().decode('utf-8') == 'file content'


def test_download_artifact_assert_status_code(client, httpx_mock, assert_response_status_mock):
    # arrange
    httpx_mock.add_response(method='GET',
                            url='https://mlaide.com/projects/pk/artifacts/a/12/files',
                            match_headers={'x-api-key': 'xyz', 'Accepts': 'application/zip'},
                            status_code=200,
                            headers={'Content-Disposition': 'attachment; filename="artifact-12.zip"'},
                            data=b'file content')

    # act
    artifact_api.download_artifact(client=client, project_key='pk', artifact_name='a', artifact_version=12)

    # assert
    assert_response_status_mock.assert_called_once()
