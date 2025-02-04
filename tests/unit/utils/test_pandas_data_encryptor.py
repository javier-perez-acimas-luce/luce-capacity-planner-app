import pandas as pd
import pytest

from app_name.utils.pandas_data_encryptor import PandasDataFrameDataEncryptor


@pytest.fixture
def data_encryptor():
    key = "test_key"
    return PandasDataFrameDataEncryptor(key=key)


def test_encrypt_columns(data_encryptor):
    df = pd.DataFrame({"value": ["test"]})
    encrypted_df = data_encryptor.encrypt_columns(df, "value", method="base64")
    decrypted_df = data_encryptor.decrypt_columns(encrypted_df, "value", method="base64")
    assert decrypted_df["value"].iloc[0] == "test"


def test_encrypt_columns_with_cast(data_encryptor):
    df = pd.DataFrame({"value": [12345]})
    encrypted_df = data_encryptor.encrypt_columns(df, "value", method="base64")
    decrypted_df = data_encryptor.decrypt_columns(encrypted_df, "value", method="base64", cast_type=int)
    assert decrypted_df["value"].iloc[0] == 12345


def test_encrypt_row(data_encryptor):
    df = pd.DataFrame({"value": ["test"]})
    encrypted_df = data_encryptor.encrypt_row(df, "value == 'test'", method="base64")
    decrypted_df = data_encryptor.decrypt_row(encrypted_df, "value == 'dGVzdA=='", method="base64")
    assert decrypted_df["value"].iloc[0] == "test"


def test_encrypt_row_with_cast(data_encryptor):
    df = pd.DataFrame({"value": [67890]})
    encrypted_df = data_encryptor.encrypt_row(df, "value == 67890", method="base64")
    decrypted_df = data_encryptor.decrypt_row(encrypted_df, "value == 'Njc4OTA='", method="base64", cast_type=int)
    assert decrypted_df["value"].iloc[0] == 67890
