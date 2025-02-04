"""
This module provides the DataEncryptor class for performing data encryption and decryption
on columns and rows of a PySpark DataFrame. It supports various encryption methods including
key-based, asymmetric, static, and Base64 encoding.

Classes:
    DataEncryptor: A class used to perform data encryption and decryption on columns and rows of a PySpark DataFrame.
"""
import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class DataEncryptor(object):
    """
    A class used to perform data encryption and decryption on columns and rows of a PySpark DataFrame.

    Attributes:
        cipher (Fernet): An instance of Fernet for key-based encryption and decryption.
        private_key (rsa.RSAPrivateKey): An instance of RSAPrivateKey for asymmetric encryption and decryption.
        public_key (rsa.RSAPublicKey): An instance of RSAPublicKey for asymmetric encryption and decryption.
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
        self.default_fixed_value = fixed_value
        self.cipher = Fernet(self._load_symmetric_key(key)) if key else None
        self.private_key = self._load_asymmetric_key(private_key_path, 'private',
                                                     private_key_password) if private_key_path else None
        self.public_key = self._load_asymmetric_key(public_key_path, 'public',
                                                    public_key_password) if public_key_path else None

    def _load_symmetric_key(self, password: str, rand: int = 0) -> bytes:
        """
        Loads a symmetric key from a password.

        Args:
            password (str): The password to use for generating the symmetric key.

        Returns:
            str: The symmetric key generated from the password.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(rand),
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def _load_asymmetric_key(self, path: str, key_type: str,
                             password: str = None) -> rsa.RSAPrivateKey or rsa.RSAPublicKey:
        """
        Loads an RSA key from a file.

        Args:
            path (str): The path to the file containing the RSA key.
            key_type (str): The type of key to load ('private' or 'public').
            password (str, optional): The password for the RSA key file. Defaults to None.

        Returns:
            rsa.RSAPrivateKey or rsa.RSAPublicKey: The RSA key loaded from the file.
        """
        with open(path, "rb") as key_file:
            key = key_file.read()
            if key_type == 'private':
                return serialization.load_pem_private_key(key, password)
            elif key_type == 'public':
                return serialization.load_pem_public_key(key, password)
            else:
                raise ValueError("Invalid key type")

    def fix_encryption(self, value, conversion: str = None) -> str:
        """
        Encrypts a given value by replacing each character with a static value.

        Args:
            conversion (str, optional): The value to replace each character with. Defaults to None.

        Returns:
            str: The encrypted value as a string.
        """
        encrypted = conversion if conversion else self.default_fixed_value
        return ''.join([encrypted for _ in value])

    def static_encryption(self, value) -> str:
        """
        Encrypts a given value using a static encryption method (simple hash).

        Args:
            value: The value to be encrypted.

        Returns:
            str: The encrypted value as a hash.
        """
        return str(hash(value))

    def key_encryption(self, value) -> str:
        """
        Encrypts a given value using key-based encryption.

        Args:
            value: The value to be encrypted.

        Returns:
            str: The encrypted value.

        Raises:
            ValueError: If the encryption key is not provided.
        """
        if not self.cipher:
            raise ValueError("Encryption key not provided")
        return self.cipher.encrypt(str(value).encode()).decode()

    def key_decryption(self, value: str, cast_type: type = str):
        """
        Decrypts a given value using key-based decryption.

        Args:
            value (str): The value to be decrypted.
            cast_type (type, optional): The type to cast the decrypted value to. Defaults to str.

        Returns:
            The decrypted value cast to the specified type.

        Raises:
            ValueError: If the encryption key is not provided.
        """
        if not self.cipher:
            raise ValueError("Decryption key not provided")
        decrypted_value = self.cipher.decrypt(value.encode()).decode()
        return cast_type(decrypted_value)

    def base64_encryption(self, value) -> str:
        """
        Encrypts a given value using Base64 encoding.

        Args:
            value: The value to be encrypted.

        Returns:
            str: The Base64 encoded value.
        """
        return base64.b64encode(str(value).encode()).decode()

    def base64_decryption(self, value: str, cast_type: type = str):
        """
        Decrypts a given value using Base64 decoding.

        Args:
            value (str): The value to be decrypted.
            cast_type (type, optional): The type to cast the decrypted value to. Defaults to str.

        Returns:
            The Base64 decoded value cast to the specified type.
        """
        decrypted_value = base64.b64decode(value.encode()).decode()
        return cast_type(decrypted_value)

    def asymmetric_encryption(self, value) -> str:
        """
        Encrypts a given value using asymmetric encryption.

        Args:
            value: The value to be encrypted.

        Returns:
            str: The encrypted value.

        Raises:
            ValueError: If the public key is not provided.
        """
        if not self.public_key:
            raise ValueError("Public key not provided")
        encrypted = self.public_key.encrypt(
            str(value).encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted.hex()

    def asymmetric_decryption(self, value: str, cast_type: type = str):
        """
        Decrypts a given value using asymmetric decryption.

        Args:
            value (str): The value to be decrypted.
            cast_type (type, optional): The type to cast the decrypted value to. Defaults to str.

        Returns:
            The decrypted value cast to the specified type.

        Raises:
            ValueError: If the private key is not provided.
        """
        if not self.private_key:
            raise ValueError("Private key not provided")
        decrypted_value = self.private_key.decrypt(
            bytes.fromhex(value),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        return cast_type(decrypted_value)
