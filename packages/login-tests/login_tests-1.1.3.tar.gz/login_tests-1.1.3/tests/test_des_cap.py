import pytest
from login_tests.utils.des_cap import get_des_cap


def test_get_des_cap_valid_input():
    """
    Prueba con entradas válidas para asegurarse de que devuelve las Desired Capabilities correctamente.
    """
    user_input = {
        "app": "path/to/app.apk",
        "platformName": "Android",
        "appium:deviceName": "emulator-5554"
    }

    expected_output = {
        "app": "path/to/app.apk",
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:noReset": True,
        "appium:newCommandTimeout": 120,
        "appium:deviceName": "emulator-5554"
    }

    result = get_des_cap(user_input)
    assert result == expected_output


def test_get_des_cap_missing_app():
    """
    Prueba que se lance una excepción si no se proporciona la clave 'app' en el input.
    """
    user_input = {
        "platformName": "Android",
        "appium:deviceName": "emulator-5554"
    }

    with pytest.raises(ValueError, match="La ruta del APK \\('app'\\) es obligatoria en las Desired Capabilities."):
        get_des_cap(user_input)


def test_get_des_cap_no_input():
    """
    Prueba que se lance una excepción si el input es None.
    """
    with pytest.raises(ValueError, match="Las Desired Capabilities son obligatorias."):
        get_des_cap(None)


def test_get_des_cap_partial_input():
    """
    Prueba con entradas parciales para asegurar que las capacidades predeterminadas sean completadas.
    """
    user_input = {
        "app": "path/to/app.apk",
        "appium:deviceName": "emulator-5554"
    }

    expected_output = {
        "app": "path/to/app.apk",
        "appium:automationName": "UiAutomator2",
        "appium:noReset": True,
        "appium:newCommandTimeout": 120,
        "appium:deviceName": "emulator-5554",
        "platformName": "Android"
    }

    result = get_des_cap(user_input)
    assert result == expected_output
