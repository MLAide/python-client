from pytest_mock.plugin import MockerFixture
from zipfile import ZipInfo
import pytest
import io

from mlaide import ModelStage
from mlaide.active_artifact import ActiveArtifact, Artifact
from mlaide._api_client.dto import ArtifactDto


@pytest.fixture
def client_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_artifact.Client')


@pytest.fixture
def active_artifact_with_loaded_artifact(client_mock, get_artifact_mock, mapper_dto_to_artifact):
    mapper_dto_to_artifact.return_value = ArtifactDto(name='a name', version=1)
    return ActiveArtifact(api_client=client_mock.return_value, project_key='project key',
                          artifact_name='a name', artifact_version=1)


@pytest.fixture
def get_artifact_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_artifact.artifact_api.get_artifact')


@pytest.fixture
def mapper_dto_to_artifact(mocker: MockerFixture):
    return mocker.patch('mlaide.active_artifact.mapper.dto_to_artifact')


@pytest.fixture
def download_artifact_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_artifact.artifact_api.download_artifact')


def test_init_should_load_artifact(client_mock, get_artifact_mock, mapper_dto_to_artifact):
    # arrange
    returned_artifact_dto = ArtifactDto()
    expected_artifact = Artifact(name='name', type='artifact type')

    get_artifact_mock.return_value = returned_artifact_dto
    mapper_dto_to_artifact.return_value = expected_artifact

    # act
    active_artifact = ActiveArtifact(api_client=client_mock.return_value, project_key='project key',
                                     artifact_name='a name', artifact_version=3, model_stage=ModelStage.STAGING)

    # assert
    assert active_artifact.artifact == expected_artifact
    get_artifact_mock.assert_called_once_with(client=client_mock.return_value,
                                              project_key='project key',
                                              artifact_name='a name',
                                              artifact_version=3,
                                              model_stage=ModelStage.STAGING.value)
    mapper_dto_to_artifact.assert_called_once_with(returned_artifact_dto)


def test_download_should_download_and_extract_zip_file(active_artifact_with_loaded_artifact: ActiveArtifact,
                                                       download_artifact_mock,
                                                       mocker: MockerFixture):
    # arrange
    zip_mock = mocker.patch('mlaide.active_artifact.ZipFile')
    zip_object = zip_mock.return_value.__enter__()

    zip_bytes = io.BytesIO(initial_bytes=bytes('abc', 'utf-8'))
    download_artifact_mock.return_value = (zip_bytes, 'artifact.zip')

    # act
    active_artifact_with_loaded_artifact.download('./any-download-target')

    # assert
    download_artifact_mock.assert_called_once_with(client=mocker.ANY, project_key='project key',
                                                   artifact_name='a name', artifact_version=1)
    zip_mock.assert_called_once_with(zip_bytes)
    zip_object.extractall.assert_called_once_with('./any-download-target')


def test_download_should_cache_downloaded_file_and_download_only_once(
        active_artifact_with_loaded_artifact: ActiveArtifact,
        download_artifact_mock,
        mocker: MockerFixture):
    # arrange
    zip_mock = mocker.patch('mlaide.active_artifact.ZipFile')

    zip_bytes = io.BytesIO(initial_bytes=bytes('abc', 'utf-8'))
    download_artifact_mock.return_value = (zip_bytes, 'artifact.zip')

    # act
    active_artifact_with_loaded_artifact.download('./download-target')
    active_artifact_with_loaded_artifact.download('./download-target-2')

    # assert
    download_artifact_mock.assert_called_once()
    assert zip_mock.call_count == 2
    assert zip_mock.call_args_list == [mocker.call(zip_bytes), mocker.call(zip_bytes)]


def test_load_model_should_load_pkl_and_deserialize_it(active_artifact_with_loaded_artifact: ActiveArtifact,
                                                       download_artifact_mock,
                                                       mocker: MockerFixture):
    # arrange
    zip_mock = mocker.patch('mlaide.active_artifact.ZipFile')
    zip_object = zip_mock.return_value.__enter__()
    zip_object.infolist.return_value = [
        ZipInfo(filename='file1.txt'),
        ZipInfo(filename='model.pkl')
    ]
    model_binary = io.BytesIO(bytes('m content', 'utf-8'))
    zip_object.open.return_value = model_binary
    bytes_ctor_mock = mocker.patch('mlaide.active_artifact.BytesIO')
    bytes_ctor_mock.return_value = model_binary

    zip_bytes = io.BytesIO(bytes('abc', 'utf-8'))
    download_artifact_mock.return_value = (zip_bytes, 'artifact.zip')

    model_deser_mock = mocker.patch('mlaide.active_artifact._model_deser')
    model_deser_mock.deserialize.return_value = 'm content'

    # act
    model = active_artifact_with_loaded_artifact.load_model()

    # assert
    assert model == 'm content'
    model_deser_mock.deserialize.assert_called_once_with(model_binary)
