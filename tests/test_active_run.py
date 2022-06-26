from pytest_mock.plugin import MockerFixture
from datetime import datetime
from os import path
import pytest
import io
from mlaide._api_client.dto.file_hash_dto import FileHashDto

from mlaide.active_run import \
    ActiveRun, get_file_hash, get_file_content, extract_filename, \
    ArtifactDto, Artifact, ArtifactRef, \
    Experiment, ExperimentDto, \
    Git, Run, RunDto, RunStatus, \
    StatusDto
from mlaide.model import model
from mlaide.model.in_memory_artifact_file import InMemoryArtifactFile
from mlaide.model.local_artifact_file import LocalArtifactFile
from mlaide.model.new_artifact import NewArtifact


@pytest.fixture
def client_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_run.Client')


@pytest.fixture
def dto_to_run_mock(mocker: MockerFixture):
    mock = mocker.patch('mlaide.active_run.dto_to_run')
    mock.return_value = Run()
    mock.return_value.key = 47
    return mock


@pytest.fixture
def dto_to_artifact_mock(mocker: MockerFixture):
    mock = mocker.patch('mlaide.active_run.dto_to_artifact')
    mock.return_value = Artifact()
    return mock


@pytest.fixture
def run_to_dto_mock(mocker: MockerFixture):
    mock = mocker.patch('mlaide.active_run.run_to_dto')
    mock.return_value = RunDto()
    mock.return_value.key = 47
    return mock


@pytest.fixture
def run_api_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_run.run_api')


@pytest.fixture
def artifact_api_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_run.artifact_api')


@pytest.fixture
def create_run_mock(run_api_mock, mocker: MockerFixture):
    run_api_mock.create_run = mocker.Mock()
    return run_api_mock.create_run


@pytest.fixture
def active_run(client_mock, create_run_mock, run_to_dto_mock, dto_to_run_mock):
    experiment = Experiment(name='my experiment')
    return ActiveRun(
        api_client=client_mock.return_value, 
        project_key='project key', 
        experiment=experiment,
        run_name='run name')


def test_init_should_create_new_run(client_mock, run_to_dto_mock, dto_to_run_mock, create_run_mock):
    # arrange
    created_run_dto = RunDto()
    create_run_mock.return_value = created_run_dto

    used_artifacts = [ArtifactRef('a name', 1)]
    git = Git(
        commit_time=datetime.now(),
        commit_hash='abc',
        repository_uri='remote repo',
        is_dirty=True
    )

    # act
    active_run = ActiveRun(api_client=client_mock.return_value,
                           project_key='project key',
                           run_name='run name',
                           experiment=Experiment(key='exp key'),
                           git=git,
                           used_artifacts=used_artifacts)

    # assert
    assert active_run.run == dto_to_run_mock.return_value

    create_run_mock.assert_called_once_with(client=client_mock.return_value,
                                            project_key='project key',
                                            run=run_to_dto_mock.return_value)

    run_to_create: Run = run_to_dto_mock.call_args[0][0]
    assert run_to_create.name == 'run name'
    assert run_to_create.git == git

    run_to_dto_mock.assert_called_once_with(run_to_create, 'exp key', used_artifacts)

    dto_to_run_mock.assert_called_once_with(created_run_dto)


def test_log_metric_should_add_metric_to_run_and_call_update_on_api(active_run, client_mock, run_api_mock):
    # arrange

    # act
    run = active_run.log_metric('the-key', 'the value')

    # assert
    assert run.metrics == {'the-key': 'the value'}
    run_api_mock.update_run_metrics.assert_called_once_with(client=client_mock.return_value,
                                                            project_key='project key',
                                                            run_key=active_run.run.key,
                                                            metrics={'the-key': 'the value'})


def test_log_metric_epoch_should_add_epoch_metric_to_run_and_call_update_on_api(active_run, client_mock, run_api_mock):
    # arrange

    # act
    run = active_run.log_metric_epoch('the-key', 'epoch-1', 'the value')
    run = active_run.log_metric_epoch('the-key', 'epoch-2', 'the value')

    # assert
    assert run.metrics == {'the-key': {
        'epoch-1': 'the value',
        'epoch-2': 'the value'
        }
    }
    expected_first_args = [({
        'client': client_mock.return_value,
        'metrics': {
            'the-key': {
                'epoch-1': 'the value'
            }
        },
        'project_key': 'project key',
        'run_key': active_run.run.key
    })]

    expected_second_args = [({
        'client': client_mock.return_value,
        'metrics': {
            'the-key': {
                'epoch-1': 'the value',
                'epoch-2': 'the value'
            }
        },
        'project_key': 'project key',
        'run_key': active_run.run.key
    })]
    assert run_api_mock.update_run_metrics.call_args_list[0] == expected_first_args
    assert run_api_mock.update_run_metrics.call_args_list[1] == expected_second_args
    assert len(run_api_mock.update_run_metrics.call_args_list) == 2


def test_log_parameter_should_add_parameter_to_run_and_call_update_on_api(active_run, client_mock, run_api_mock):
    # arrange

    # act
    run = active_run.log_parameter('the-key', 3)

    # assert
    assert run.parameters == {'the-key': 3}
    run_api_mock.update_run_parameters.assert_called_once_with(client=client_mock.return_value,
                                                               project_key='project key',
                                                               run_key=active_run.run.key,
                                                               parameters={'the-key': 3})


def test_log_model_should_create_an_artifact_and_attach_the_serialized_model_as_file(active_run,
                                                                                     client_mock,
                                                                                     artifact_api_mock,
                                                                                     dto_to_artifact_mock,
                                                                                     run_api_mock,
                                                                                     mocker: MockerFixture):
    # arrange
    serialized_files = [InMemoryArtifactFile('model.pkl', io.BytesIO(bytes('foo', 'utf-8')))]
    model_serializer_mock = mocker.patch('mlaide.active_run._model_deser')
    model_serializer_mock.serialize.return_value = serialized_files

    get_file_hash_mock = mocker.patch('mlaide.active_run.get_file_hash')
    get_file_hash_mock.return_value = '123456'

    created_artifact_dto = ArtifactDto(name='x', version=3)
    artifact_api_mock.find_artifact_by_file_hashes.return_value = created_artifact_dto

    created_artifact = Artifact(name='a name', version=15)
    dto_to_artifact_mock.return_value = created_artifact
    
    # act
    active_run.log_model('the model content', 'my-model', {'k': 'v'})

    # assert
    artifact_api_mock.find_artifact_by_file_hashes.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='my-model',
        files=['123456'])
    run_api_mock.attach_artifact_to_run.assert_called_once_with(
        client=client_mock.return_value,
        artifact_name='x',
        artifact_version=3,
        project_key='project key',
        run_key=47)
    artifact_api_mock.create_model.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='a name',
        artifact_version=15)


def test_add_artifact_should_create_an_artifact_with_files_from_memory_if_same_artifact_does_not_exist(
    client_mock, 
    active_run, 
    artifact_api_mock,
    dto_to_artifact_mock,
    mocker: MockerFixture):

    # arrange
    get_file_hash_mock = mocker.patch('mlaide.active_run.get_file_hash')
    get_file_hash_mock.return_value = FileHashDto('data.txt', '123abc')

    artifact_api_mock.find_artifact_by_file_hashes.return_value = None

    created_artifact_dto = ArtifactDto(name='created artifact dto')
    artifact_api_mock.create_artifact.return_value = created_artifact_dto

    created_artifact = Artifact(name='created artifact', version=2)
    dto_to_artifact_mock.return_value = created_artifact
    
    file_content = io.BytesIO(bytes('foo', 'utf-8'))
    files = [InMemoryArtifactFile('data.txt', file_content)]
    artifact = NewArtifact('my artifact', 'dataset', files)

    # act
    active_run.add_artifact(artifact)

    # assert
    artifact_api_mock.find_artifact_by_file_hashes.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='my artifact',
        files=[FileHashDto('data.txt', '123abc')])
    artifact_api_mock.create_artifact.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact=ArtifactDto(name='my artifact', type='dataset', metadata=None, run_key=47))
    artifact_api_mock.upload_file.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='created artifact',
        artifact_version=2,
        filename='data.txt',
        file_hash='123abc',
        file=file_content)


def test_add_artifact_should_create_an_artifact_with_files_from_local_filesystem_if_same_artifact_does_not_exist(
    client_mock, 
    active_run, 
    artifact_api_mock,
    dto_to_artifact_mock,
    mocker: MockerFixture):

    # arrange
    get_file_hash_mock = mocker.patch('mlaide.active_run.get_file_hash')
    get_file_hash_mock.return_value = FileHashDto('data.txt', '123abc')

    artifact_api_mock.find_artifact_by_file_hashes.return_value = None

    created_artifact_dto = ArtifactDto(name='created artifact dto')
    artifact_api_mock.create_artifact.return_value = created_artifact_dto

    created_artifact = Artifact(name='created artifact', version=2)
    dto_to_artifact_mock.return_value = created_artifact

    extract_filename_mock = mocker.patch('mlaide.active_run.extract_filename')
    extract_filename_mock.return_value = 'data.txt'

    file_content = io.BytesIO(bytes('foo', 'utf-8'))
    get_file_content_mock = mocker.patch('mlaide.active_run.get_file_content')
    get_file_content_mock.return_value = file_content
    
    files = [LocalArtifactFile('/current-working-directory/data.txt')]
    artifact = NewArtifact('my artifact', 'dataset', files)

    # act
    active_run.add_artifact(artifact)

    # assert
    artifact_api_mock.find_artifact_by_file_hashes.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='my artifact',
        files=[FileHashDto('data.txt', '123abc')])
    artifact_api_mock.create_artifact.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact=ArtifactDto(name='my artifact', type='dataset', metadata=None, run_key=47))
    artifact_api_mock.upload_file.assert_called_once_with(
        client=client_mock.return_value,
        project_key='project key',
        artifact_name='created artifact',
        artifact_version=2,
        filename='data.txt',
        file_hash='123abc',
        file=file_content)


def test_set_completed_status_should_set_status_and_end_time_in_run(active_run, mocker: MockerFixture):
    # arrange
    now = datetime.now()
    datetime_mock = mocker.patch('mlaide.active_run.datetime')
    datetime_mock.now.return_value = now

    # act
    run = active_run.set_completed_status()

    # assert
    assert run.end_time == now
    assert active_run.run.end_time == now
    assert run.status == RunStatus.COMPLETED
    assert active_run.run.status == RunStatus.COMPLETED


def test_set_completed_status_should_invoke_run_api_with_new_status(active_run,
                                                                    run_api_mock,
                                                                    client_mock,
                                                                    mocker: MockerFixture):
    # arrange
    now = datetime.now()
    datetime_mock = mocker.patch('mlaide.active_run.datetime')
    datetime_mock.now.return_value = now

    # act
    active_run.set_completed_status()

    # assert
    run_api_mock.partial_update_run.assert_called_once_with(client=client_mock.return_value,
                                                            project_key='project key',
                                                            run_key=47,
                                                            run=RunDto(status=StatusDto.COMPLETED))


def test_set_failed_status_should_set_status_and_end_time_in_run(active_run, mocker: MockerFixture):
    # arrange
    now = datetime.now()
    datetime_mock = mocker.patch('mlaide.active_run.datetime')
    datetime_mock.now.return_value = now

    # act
    run = active_run.set_failed_status()

    # assert
    assert run.end_time == now
    assert active_run.run.end_time == now
    assert run.status == RunStatus.FAILED
    assert active_run.run.status == RunStatus.FAILED


def test_set_failed_status_should_invoke_run_api_with_new_status(active_run,
                                                                 run_api_mock,
                                                                 client_mock,
                                                                 mocker: MockerFixture):
    # arrange
    now = datetime.now()
    datetime_mock = mocker.patch('mlaide.active_run.datetime')
    datetime_mock.now.return_value = now

    # act
    active_run.set_failed_status()

    # assert
    run_api_mock.partial_update_run.assert_called_once_with(client=client_mock.return_value,
                                                            project_key='project key',
                                                            run_key=47,
                                                            run=RunDto(status=StatusDto.FAILED))


def test_get_file_hash_should_return_file_hash_of_InMemoryArtifactFile(mocker: MockerFixture):
    # arrange
    file_content = io.BytesIO(bytes('aaa', 'utf-8'))
    file = InMemoryArtifactFile('data.txt', file_content)
    file_utils_mock = mocker.patch('mlaide.active_run._file_utils')
    file_utils_mock.calculate_checksum_of_bytes.return_value = '1234'

    # act
    hash = get_file_hash(file)

    # assert
    assert hash is not None
    assert hash.fileName == 'data.txt'
    assert hash.fileHash == '1234'
    file_utils_mock.calculate_checksum_of_bytes.assert_called_once_with(file_content)


def test_get_file_hash_should_return_file_hash_of_LocalArtifactFile(mocker: MockerFixture):
    # arrange
    file = LocalArtifactFile('data.txt')
    file_utils_mock = mocker.patch('mlaide.active_run._file_utils')
    file_utils_mock.calculate_checksum_of_file.return_value = '1234'
    getcwd_mock = mocker.patch('mlaide.active_run.getcwd')
    getcwd_mock.return_value = '/path/to/file'

    # act
    hash = get_file_hash(file)

    # assert
    assert hash is not None
    assert hash.fileName == 'data.txt'
    assert hash.fileHash == '1234'
    file_utils_mock.calculate_checksum_of_file.assert_called_once_with('/path/to/file/data.txt')
