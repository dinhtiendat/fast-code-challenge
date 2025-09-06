import base64
from fastapi import HTTPException
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from app.utils.logs import logger
from app.core.config import settings


key = bytes(settings.SECRET_KEY, 'utf-8')


def aes_encode(plain_text: str) -> str:
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(cipher_text).decode('utf-8')


def aes_decode(cipher_text: str) -> str:
    try:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()
        cipher_text = base64.b64decode(cipher_text.encode('utf-8'))
        decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plain_text = unpadder.update(decrypted_data) + unpadder.finalize()
        return plain_text.decode('utf-8')
    except Exception as e:
        logger.error("aes_decode error: " + str(e), extra={"status_code": 500})
        raise HTTPException(status_code=500, detail="aes decode error")
