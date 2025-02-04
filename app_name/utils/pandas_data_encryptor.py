"""
This module provides the PandasDataEncryptor class for performing data encryption and decryption
on columns and rows of a Pandas DataFrame. It supports various encryption methods including
key-based, asymmetric, static, and Base64 encoding.

Classes:
    PandasDataEncryptor: A class used to perform data encryption and decryption on columns and rows of a Pandas DataFrame.
"""
import pandas as pd

from .data_encryptor import DataEncryptor


class PandasDataFrameDataEncryptor(DataEncryptor):
    """
    A class used to perform data encryption and decryption on columns and rows of a pandas DataFrame.
    """

    def __init__(self, key: str = None, fixed_value: str = '*',
                 private_key_path: str = None, public_key_path: str = None,
                 private_key_password: str = None, public_key_password: str = None):
        """
        Initializes the DataEncryptor with an optional encryption key and RSA keys.

        Args:
            key (str, optional): The encryption key. If not provided, key-based encryption will not be available.
            fixed_value (str, optional): The fixed value to use for static encryption. Defaults to '***'.
            private_key_path (str, optional): The path to the RSA private key file.
            public_key_path (str, optional): The path to the RSA public key file.
            private_key_password (str, optional): The password for the RSA private key file.
            public_key_password (str, optional): The password for the RSA public key file.
        """
        super().__init__(key, fixed_value, private_key_path, public_key_path, private_key_password, public_key_password)

    def _encrypt_column(self, df: pd.DataFrame, column_name: str, method: str = 'fix'):
        """
        Encrypts a specified column in the DataFrame using the given encryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to be encrypted.
            column_name (str): The name of the column to be encrypted.
            method (str, optional): The encryption method to use ('static', 'key', 'asymmetric', 'fix', or 'base64'). Defaults to 'fix'.

        Returns:
            pd.DataFrame: The DataFrame with the encrypted column.

        Raises:
            ValueError: If an unsupported encryption method is provided.
        """
        if method == 'static':
            df[column_name] = df[column_name].apply(self.static_encryption)
        elif method == 'key':
            df[column_name] = df[column_name].apply(self.key_encryption)
        elif method == 'asymmetric':
            df[column_name] = df[column_name].apply(self.asymmetric_encryption)
        elif method == 'fix':
            df[column_name] = df[column_name].apply(self.fix_encryption)
        elif method == 'base64':
            df[column_name] = df[column_name].apply(self.base64_encryption)
        else:
            raise ValueError("Unsupported encryption method")
        return df

    def _decrypt_column(self, df: pd.DataFrame, column_name: str, method: str = 'key', cast_type: type = str):
        """
        Decrypts a specified column in the DataFrame using the given decryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the column to be decrypted.
            column_name (str): The name of the column to be decrypted.
            method (str, optional): The decryption method to use ('key', 'asymmetric', or 'base64'). Defaults to 'key'.
            cast_type (type, optional): The type to cast the decrypted value to. Defaults to str.

        Returns:
            pd.DataFrame: The DataFrame with the decrypted column.

        Raises:
            ValueError: If an unsupported decryption method is provided.
        """
        if method == 'key':
            df[column_name] = df[column_name].apply(lambda x: self.key_decryption(x, cast_type))
        elif method == 'asymmetric':
            df[column_name] = df[column_name].apply(lambda x: self.asymmetric_decryption(x, cast_type))
        elif method == 'base64':
            df[column_name] = df[column_name].apply(lambda x: self.base64_decryption(x, cast_type))
        else:
            raise ValueError("Unsupported decryption method")
        return df

    def encrypt_columns(self, df: pd.DataFrame, columns, method: str = 'fix'):
        """
        Encrypts specified columns in the DataFrame using the given encryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the columns to be encrypted.
            columns (Union[list, str]): The list of columns or a single column to be encrypted.
            method (str, optional): The encryption method to use ('static', 'key', 'asymmetric', 'fix', or 'base64'). Defaults to 'fix'.

        Returns:
            pd.DataFrame: The DataFrame with the encrypted columns.

        Raises:
            ValueError: If an unsupported encryption method is provided.
        """
        if isinstance(columns, str):
            columns = [columns]

        for col in columns:
            df = self._encrypt_column(df, col, method)
        return df

    def decrypt_columns(self, df: pd.DataFrame, columns, method: str = 'key', cast_type: type = str):
        """
        Decrypts specified columns in the DataFrame using the given decryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the columns to be decrypted.
            columns (Union[list, str]): The list of columns or a single column to be decrypted.
            method (str, optional): The decryption method to use ('key', 'asymmetric', or 'base64'). Defaults to 'key'.
            cast_type (type, optional): The type to cast the decrypted values to. Defaults to str.

        Returns:
            pd.DataFrame: The DataFrame with the decrypted columns.

        Raises:
            ValueError: If an unsupported decryption method is provided.
        """
        if isinstance(columns, str):
            columns = [columns]

        for col in columns:
            df = self._decrypt_column(df, col, method, cast_type)
        return df

    def encrypt_row(self, df: pd.DataFrame, filter_condition: str, method: str = 'fix', skip_columns: list = []):
        """
        Encrypts rows in the DataFrame based on a filter condition using the given encryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the rows to be encrypted.
            filter_condition (str): The filter condition to select rows to be encrypted.
            method (str, optional): The encryption method to use ('static', 'key', 'asymmetric', 'fix', or 'base64'). Defaults to 'fix'.
            skip_columns (list, optional): List of columns to skip during encryption. Defaults to [].

        Returns:
            pd.DataFrame: The DataFrame with the encrypted rows added as new rows and original rows removed.

        Raises:
            ValueError: If an unsupported encryption method is provided.
        """
        filtered_df = df.query(filter_condition)
        encrypted_df = filtered_df.copy()

        for col in df.columns:
            if col not in skip_columns:
                encrypted_df = self._encrypt_column(encrypted_df, col, method)

        df = df.drop(filtered_df.index)
        return pd.concat([df, encrypted_df])

    def decrypt_row(self, df: pd.DataFrame, filter_condition: str, method: str = 'key', skip_columns: list = [],
                    cast_type: type = str):
        """
        Decrypts rows in the DataFrame based on a filter condition using the given decryption method.

        Args:
            df (pd.DataFrame): The DataFrame containing the rows to be decrypted.
            filter_condition (str): The filter condition to select rows to be decrypted.
            method (str, optional): The decryption method to use ('key', 'asymmetric', or 'base64'). Defaults to 'key'.
            skip_columns (list, optional): List of columns to skip during decryption. Defaults to [].
            cast_type (type, optional): The type to cast the decrypted values to. Defaults to str.

        Returns:
            pd.DataFrame: The DataFrame with the decrypted rows added as new rows and original rows removed.

        Raises:
            ValueError: If an unsupported decryption method is provided.
        """
        filtered_df = df.query(filter_condition)
        decrypted_df = filtered_df.copy()

        for col in df.columns:
            if col not in skip_columns:
                decrypted_df = self._decrypt_column(decrypted_df, col, method, cast_type)

        df = df.drop(filtered_df.index)
        return pd.concat([df, decrypted_df])
