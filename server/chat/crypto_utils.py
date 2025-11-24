import base64
import os
from functools import lru_cache
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings
import pyotp
from secrets import token_bytes


# 마스터키 가져오기 (.env의 MASTER_KEY_B64에 의존)
@lru_cache(maxsize=1)
def get_master_key() -> bytes:
    key = getattr(settings, "MASTER_KEY", None)
    if key is None:
        b64_key = os.environ.get("MASTER_KEY_B64")
        if b64_key:
            try:
                key = base64.b64decode(b64_key)
            except Exception as exc:
                raise RuntimeError("MASTER_KEY_B64 is not valid base64") from exc

    if key is None or len(key) not in (16, 24, 32):
        raise RuntimeError("MASTER_KEY not configured in settings or .env")
    return key

# 의사 난수 생성
def generate_pseudo_number():
    secret_key = token_bytes(32) # 채팅방 고유 비밀키
    iv = token_bytes(12) # 초기화 벡터 (12 Bytes 권장)

    return secret_key, iv

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
