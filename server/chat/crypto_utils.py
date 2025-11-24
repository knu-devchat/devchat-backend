import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from secrets import token_bytes
from .crypto_helpers import get_master_key


# 의사 난수 생성
def generate_pseudo_number():
    raw = token_bytes(16)
    secret_b32 = base64.b32encode(raw).decode('ascii')  # ASCII base32 string
    secret_bytes = secret_b32.encode('utf-8')
    iv = token_bytes(12)  # 12 bytes recommended for AES-GCM

    return secret_bytes, iv


# AES-GCM 암호화 및 Base64 인코딩
def encrypt_aes_gcm(secret_key: bytes, iv: bytes) -> str:
    master_key = get_master_key()
    aesgcm = AESGCM(master_key)
    ciphertext = aesgcm.encrypt(iv, secret_key, None)
    return base64.b64encode(iv + ciphertext).decode()


# Base64 디코딩 및 AES-GCM 복호화
def decrypt_aes_gcm(b64_data: str) -> bytes:
    master_key = get_master_key()
    data = base64.b64decode(b64_data)
    iv = data[:12]
    ciphertext = data[12:]
    aesgcm = AESGCM(master_key)
    return aesgcm.decrypt(iv, ciphertext, None)