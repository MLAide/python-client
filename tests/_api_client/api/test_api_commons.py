from pytest import raises
from pytest_mock import MockerFixture

from mlaide.error import *
from mlaide._api_client.api._api_commons import assert_response_status


def test_assert_response_status_with_404_response_and_404_is_allowed_should_not_raise(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 404

    # act
    assert_response_status(response, True)


def test_assert_response_status_with_404_response_should_raise_not_found_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 404

    # act
    with raises(NotFoundError):
        assert_response_status(response)


def test_assert_response_status_with_400_response_should_raise_input_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 400

    # act
    with raises(InputError):
        assert_response_status(response)


def test_assert_response_status_with_401_response_should_raise_invalid_authorization_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 401

    # act
    with raises(InvalidAuthorizationError):
        assert_response_status(response)


def test_assert_response_status_with_403_response_should_raise_not_authorized_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 403

    # act
    with raises(NotAuthorizedError):
        assert_response_status(response)


def test_assert_response_status_with_500_response_should_raise_server_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 500

    # act
    with raises(ServerError):
        assert_response_status(response)


def test_assert_response_status_with_501_response_should_raise_server_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 501

    # act
    with raises(ServerError):
        assert_response_status(response)


def test_assert_response_status_with_502_response_should_raise_server_error(mocker: MockerFixture):
    # arrange
    response = mocker.MagicMock()
    response.status_code = 502

    # act
    with raises(ServerError):
        assert_response_status(response)
