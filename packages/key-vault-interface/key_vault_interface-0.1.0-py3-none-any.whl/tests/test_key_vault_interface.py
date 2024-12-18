import pytest

from unittest.mock import MagicMock, patch
from key_vault_interface.key_vault_interface import KeyVaultInterface


# Mock configuration data
mock_secrets_to_load = {
    "secret_1": "test_secret_1",
    "secret_2": "test_secret_2"
}

# Mock of SecretClient and response from Azure
mock_secret = MagicMock()
mock_secret.properties.expires_on = None
mock_secret.properties.not_before = None
mock_secret.value = "mock_secret_value"
mock_secret.properties.content_type = "text"

@pytest.fixture
def key_vault_interface():
    with patch('my_keyvault_interface.keyvault_interface.SecretClient', autospec=True):
        # Create an instance of the class with mocked secrets
        return KeyVaultInterface(secrets_to_load=mock_secrets_to_load)


def test_keyvault_interface_initialization(key_vault_interface):
    # Check that the KeyVaultInterface is initialized correctly
    assert isinstance(key_vault_interface, KeyVaultInterface)
    assert key_vault_interface.loaded_secrets == {}
    assert key_vault_interface.secrets_to_load == mock_secrets_to_load


def test_load_secret(key_vault_interface):
    # Test loading a secret
    with patch('my_keyvault_interface.keyvault_interface.key_vault_client.get_secret') as mock_get_secret:
        mock_get_secret.return_value = mock_secret  # Simulate getting a secret
        key_vault_interface._load_secret("secret_1", "test_secret_1")

        # Verify the secret was loaded and added to the loaded_secrets
        assert "secret_1" in key_vault_interface.loaded_secrets
        assert key_vault_interface.loaded_secrets["secret_1"] == "mock_secret_value"


def test_get_secret(key_vault_interface):
    # Test retrieving a loaded secret
    with patch('my_keyvault_interface.keyvault_interface.key_vault_client.get_secret') as mock_get_secret:
        mock_get_secret.return_value = mock_secret
        key_vault_interface._load_secret("secret_1", "test_secret_1")
        
        secret_value = key_vault_interface.get("secret_1")
        assert secret_value == "mock_secret_value"


def test_forget_secret(key_vault_interface):
    # Test forgetting a secret
    with patch('my_keyvault_interface.keyvault_interface.key_vault_client.get_secret') as mock_get_secret:
        mock_get_secret.return_value = mock_secret
        key_vault_interface._load_secret("secret_1", "test_secret_1")
        
        # Forget the secret and check it's removed
        key_vault_interface.forget_secret("secret_1")
        assert "secret_1" not in key_vault_interface.loaded_secrets


def test_get_secret_not_found(key_vault_interface):
    # Test getting a secret that isn't loaded
    result = key_vault_interface.get("non_existent_secret")
    assert result is None  # It should return None if not found


def test_update_and_reload_secrets(key_vault_interface):
    # Test updating and reloading secrets
    new_secrets = {"secret_3": "test_secret_3"}
    key_vault_interface.update_and_reload_secrets(new_secrets)
    
    # Verify the new secret was added
    assert "secret_3" in key_vault_interface.secrets_to_load
    assert key_vault_interface.secrets_to_load["secret_3"] == "test_secret_3"
