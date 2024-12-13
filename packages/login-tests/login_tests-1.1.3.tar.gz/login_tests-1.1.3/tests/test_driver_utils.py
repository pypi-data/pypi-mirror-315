from unittest.mock import MagicMock
from login_tests.utils.driver_utils import initialize_driver
import pytest

def test_initialize_driver_valid_input():
    # Simula un user_input válido
    mock_user_input = {
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "app": "dummy.apk"
    }

    # Mockea el objeto WebDriver de Appium
    mock_driver = MagicMock()
    with pytest.MonkeyPatch().context() as m:
        m.setattr("appium.webdriver.Remote", MagicMock(return_value=mock_driver))
        driver = initialize_driver(mock_user_input)

    assert driver is not None  # Asegura que se retorna un objeto
    assert mock_driver.implicitly_wait.called  # Verifica que se llamó a `implicitly_wait`

def test_initialize_driver_no_input():
    # Valida que lance ValueError si no se pasa `user_input`
    with pytest.raises(ValueError, match="Las Desired Capabilities son obligatorias."):
        initialize_driver(None)
