from pytest_mock.plugin import MockerFixture
from datetime import datetime
from os import path
import pytest
import io

from mlaide.active_run import \
    ActiveRun, \
    ArtifactDto, Artifact, ArtifactRef, \
    ExperimentDto, ExperimentStatusDto, \
    Git, Run, RunDto, RunStatus, \
    StatusDto


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
def experiment_api_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_run.experiment_api')


@pytest.fixture
def artifact_api_mock(mocker: MockerFixture):
    return mocker.patch('mlaide.active_run.artifact_api')


@pytest.fixture
def create_run_mock(run_api_mock, mocker: MockerFixture):
    run_api_mock.create_run = mocker.Mock()
    return run_api_mock.create_run


@pytest.fixture
def active_run(client_mock, create_run_mock, run_to_dto_mock, dto_to_run_mock):
    return ActiveRun(
        client_mock.return_value, 'project key', 'run name', Git(), 'exp key', auto_create_experiment=False)


def test_init_should_create_new_run(client_mock, run_to_dto_mock, dto_to_run_mock, create_run_mock):
    # arrange
    created_run_dto = RunDto()
    create_run_mock.return_value = created_run_dto

    used_artifact = [ArtifactRef('a name', 1)]
    git = Git(
        commit_time=datetime.now(),
        commit_hash='abc',
        repository_url='remote repo',
        is_dirty=True
    )

    # act
    active_run = ActiveRun(client_mock.return_value, 'project key',
                           'run name', git, 'exp key', used_artifact, auto_create_experiment=False)

    # assert
    assert active_run.run == dto_to_run_mock.return_value

    create_run_mock.assert_called_once_with(client=client_mock.return_value,
                                            project_key='project key',
                                            run=run_to_dto_mock.return_value)

    run_to_create: Run = run_to_dto_mock.call_args[0][0]
    assert run_to_create.name == 'run name'
    assert run_to_create.git == git

    run_to_dto_mock.assert_called_once_with(run_to_create, 'exp key', used_artifact)

    dto_to_run_mock.assert_called_once_with(created_run_dto)


def test_init_auto_create_experiment_is_true_and_experiment_key_is_none_should_not_create_new_experiment(
        client_mock,
        run_to_dto_mock,
        dto_to_run_mock,
        create_run_mock,
        experiment_api_mock):
    # arrange
    created_run_dto = RunDto()
    create_run_mock.return_value = created_run_dto

    # act
    ActiveRun(api_client=client_mock.return_value,
              project_key='project key',
              run_name='run name',
              git=Git(),
              experiment_key=None,
              auto_create_experiment=True)

    # assert
    experiment_api_mock.get_experiment.assert_not_called()
    experiment_api_mock.create_experiment.assert_not_called()


def test_init_auto_create_experiment_is_true_and_specified_experiment_key_exists_should_not_create_new_experiment(
        client_mock,
        run_to_dto_mock,
        dto_to_run_mock,
        create_run_mock,
        experiment_api_mock):
    # arrange
    created_run_dto = RunDto()
    create_run_mock.return_value = created_run_dto
    experiment_api_mock.get_experiment.return_value = ExperimentDto()

    # act
    ActiveRun(api_client=client_mock.return_value,
              project_key='project key',
              run_name='run name',
              git=Git(),
              experiment_key='exp key',
              auto_create_experiment=True)

    # assert
    experiment_api_mock.get_experiment.assert_called_once_with(client=client_mock.return_value,
                                                               project_key='project key', experiment_key='exp key')
    experiment_api_mock.create_experiment.assert_not_called()


def test_init_auto_create_experiment_is_true_and_specified_experiment_key_does_not_exist_should_create_new_experiment(
        client_mock,
        run_to_dto_mock,
        dto_to_run_mock,
        create_run_mock,
        experiment_api_mock):
    # arrange
    created_run_dto = RunDto()
    create_run_mock.return_value = created_run_dto
    experiment_api_mock.get_experiment.return_value = None

    expected_experiment_to_create = ExperimentDto(key='exp key', name='exp key', status=ExperimentStatusDto.IN_PROGRESS)

    # act
    ActiveRun(api_client=client_mock.return_value,
              project_key='project key',
              run_name='run name',
              git=Git(),
              experiment_key='exp key',
              auto_create_experiment=True)

    # assert
    experiment_api_mock.get_experiment.assert_called_once_with(client=client_mock.return_value,
                                                               project_key='project key', experiment_key='exp key')
    experiment_api_mock.create_experiment.assert_called_once_with(client=client_mock.return_value,
                                                                  project_key='project key',
                                                                  experiment=expected_experiment_to_create)


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
                                                                                     mocker: MockerFixture):
    # arrange
    serialized_model = io.BytesIO(bytes('foo', 'utf-8'))

    model_serializer_mock = mocker.patch('mlaide.active_run._model_deser')
    model_serializer_mock.serialize.return_value = serialized_model

    created_artifact_dto = ArtifactDto()
    artifact_api_mock.create_artifact.return_value = created_artifact_dto

    created_artifact = Artifact(name='a name', version=15)
    dto_to_artifact_mock.return_value = created_artifact
    
    # act
    active_run.log_model('the model content', 'my-model', {'k': 'v'})

    # assert
    expected_artifact_to_create = ArtifactDto(name='my-model', type='model', metadata={'k': 'v'}, run_key=47)
    artifact_api_mock.create_artifact.assert_called_once_with(client=client_mock.return_value,
                                                              project_key='project key',
                                                              artifact=expected_artifact_to_create)
    artifact_api_mock.upload_file.assert_called_once_with(client=client_mock.return_value,
                                                          project_key='project key',
                                                          artifact_name='a name',
                                                          artifact_version=15,
                                                          filename='model.pkl',
                                                          file=serialized_model)
    artifact_api_mock.create_model.assert_called_once_with(client=client_mock.return_value,
                                                           project_key='project key',
                                                           artifact_name='a name',
                                                           artifact_version=15)
    model_serializer_mock.serialize.assert_called_once_with('the model content')


def test_create_artifact_should_create_an_artifact(active_run,
                                                   client_mock,
                                                   artifact_api_mock,
                                                   dto_to_artifact_mock):
    # arrange
    created_artifact_dto = ArtifactDto()
    artifact_api_mock.create_artifact.return_value = created_artifact_dto

    created_artifact = Artifact(name='a name', version=15)
    dto_to_artifact_mock.return_value = created_artifact

    # act
    artifact = active_run.create_artifact('artifact name', 'the type', {'k': 'val'})

    # assert
    assert artifact == created_artifact
    expected_artifact_to_create = ArtifactDto(name='artifact name', type='the type', metadata={'k': 'val'}, run_key=47)
    artifact_api_mock.create_artifact.assert_called_once_with(client=client_mock.return_value,
                                                              project_key='project key',
                                                              artifact=expected_artifact_to_create)
    dto_to_artifact_mock.assert_called_once_with(created_artifact_dto)


def test_add_artifact_file_of_type_bytes_io_should_upload_a_file(active_run,
                                                                 client_mock,
                                                                 artifact_api_mock):
    # arrange
    file = io.BytesIO(bytes('foo', 'utf-8'))
    artifact = Artifact(name='artifact name', version=23)

    # act
    active_run.add_artifact_file(artifact, file, 'my-file.txt')

    # assert
    artifact_api_mock.upload_file.assert_called_once_with(client=client_mock.return_value,
                                                          project_key='project key',
                                                          artifact_name='artifact name',
                                                          artifact_version=23,
                                                          filename='my-file.txt',
                                                          file=file)


def test_add_artifact_file_of_type_bytes_io_without_filename_should_raise_exception(active_run):
    # arrange
    file = io.BytesIO(bytes('foo', 'utf-8'))
    artifact = Artifact(name='artifact name', version=23)

    # act
    with pytest.raises(Exception):
        active_run.add_artifact_file(artifact, file, 'my-file.txt')


def test_add_artifact_file_of_type_str_should_read_file_from_disc_and_upload_it(active_run,
                                                                                client_mock,
                                                                                artifact_api_mock,
                                                                                mocker: MockerFixture):
    # arrange
    file_path = path.normpath('path/to/file.txt')
    file_bytes = bytes('foo', 'utf-8')
    file = io.BytesIO(file_bytes)
    artifact = Artifact(name='artifact name', version=23)

    path_mock = mocker.patch('mlaide.active_run.Path')
    path_mock.return_value.is_file.return_value = True
    path_mock.return_value.read_bytes.return_value = file_bytes

    bytes_io_mock = mocker.patch('mlaide.active_run.BytesIO')
    bytes_io_mock.return_value = file

    # act
    active_run.add_artifact_file(artifact, file_path)

    # assert
    artifact_api_mock.upload_file.assert_called_once_with(client=client_mock.return_value,
                                                          project_key='project key',
                                                          artifact_name='artifact name',
                                                          artifact_version=23,
                                                          filename=file_path,
                                                          file=file)
    path_mock.assert_called_once_with(file_path)
    bytes_io_mock.assert_called_once_with(file_bytes)


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
