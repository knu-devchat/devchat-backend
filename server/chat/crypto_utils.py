import base64
import pyotp
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .crypto_helpers import get_master_key
from os import environ
from secrets import token_bytes
from dotenv import load_dotenv
load_dotenv()

# 의사 난수 생성
def generate_pseudo_number():
    secret_key = pyotp.random_base32() # Base32 문자열 (totp는 base32 인코딩이 표준)
    iv = token_bytes(12)

    return secret_key, iv

# AES-GCM 암호화 및 Base64 인코딩
def encrypt_aes_gcm(secret_key: str, iv: bytes) -> str:
    master_key = get_master_key()
    aesgcm = AESGCM(master_key)
    ciphertext = aesgcm.encrypt(iv, secret_key.encode(), None)
    return base64.b64encode(iv + ciphertext).decode()

# Base64 디코딩 및 AES-GCM 복호화
def decrypt_aes_gcm(b64_data: str) -> str:
    master_key = get_master_key()
    data = base64.b64decode(b64_data)
    iv = data[:12]
    ciphertext = data[12:]
    aesgcm = AESGCM(master_key)
    secret_key_bytes = aesgcm.decrypt(iv, ciphertext, None)
    return secret_key_bytes.decode() # Base32 문자열