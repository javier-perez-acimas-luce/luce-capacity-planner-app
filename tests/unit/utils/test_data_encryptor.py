import pytest

from app_name.utils.data_encryptor import DataEncryptor


@pytest.fixture
def data_encryptor():
    key = "test_key"
    return DataEncryptor(key=key)


def test_fix_encryption(data_encryptor):
    value = "test"
    encrypted_value = data_encryptor.fix_encryption(value, conversion="*")
    assert encrypted_value == "****"


def test_static_encryption(data_encryptor):
    value = "test"
    encrypted_value = data_encryptor.static_encryption(value)
    assert encrypted_value == str(hash(value))


def test_key_encryption(data_encryptor):
    value = "test"
    encrypted_value = data_encryptor.key_encryption(value)
    decrypted_value = data_encryptor.key_decryption(encrypted_value)
    assert decrypted_value == value


def test_key_encryption_with_cast(data_encryptor):
    value = 12345
    encrypted_value = data_encryptor.key_encryption(value)
    decrypted_value = data_encryptor.key_decryption(encrypted_value, cast_type=int)
    assert decrypted_value == value


def test_base64_encryption(data_encryptor):
    value = "test"
    encrypted_value = data_encryptor.base64_encryption(value)
    decrypted_value = data_encryptor.base64_decryption(encrypted_value)
    assert decrypted_value == value


def test_base64_encryption_with_cast(data_encryptor):
    value = 123.45
    encrypted_value = data_encryptor.base64_encryption(value)
    decrypted_value = data_encryptor.base64_decryption(encrypted_value, cast_type=float)
    assert decrypted_value == value


def test_asymmetric_encryption(data_encryptor):
    private_key = data_encryptor.private_key
    public_key = data_encryptor.public_key
    if private_key and public_key:
        value = "test"
        encrypted_value = data_encryptor.asymmetric_encryption(value)
        decrypted_value = data_encryptor.asymmetric_decryption(encrypted_value)
        assert decrypted_value == value


def test_asymmetric_encryption_with_cast(data_encryptor):
    private_key = data_encryptor.private_key
    public_key = data_encryptor.public_key
    if private_key and public_key:
        value = 67890
        encrypted_value = data_encryptor.asymmetric_encryption(value)
        decrypted_value = data_encryptor.asymmetric_decryption(encrypted_value, cast_type=int)
        assert decrypted_value == value
