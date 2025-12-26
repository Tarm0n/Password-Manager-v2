import os
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def derive_key(password:str, salt:bytes):
    """Derives the key for encryption/decryption\n
    Uses SHA256 for hashing"""
    pw = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000
    )
    return kdf.derive(pw)


def encrypt(master_password:str, data:str):
    """Encrypts the given password with the master password for the password manager"""
    salt = os.urandom(16)
    key = derive_key(master_password, salt)


    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data.encode(), associated_data=None)

    return salt + nonce + ct


def decrypt(master_password:str, ciphertext:bytes):
    """Decrypts the encrypted password with the master password for the password manager"""
    salt = ciphertext[:16]
    nonce = ciphertext[16:28]
    ct = ciphertext[28:]

    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)

    #if user has given a wrong master password, it will lead to an InvalidTag error
    try:
        plain_bytes = aesgcm.decrypt(nonce, ct, associated_data=None)
        return plain_bytes.decode()
    except cryptography.exceptions.InvalidTag:
        return None