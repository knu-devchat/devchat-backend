import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .utils import get_master_key
from os import environ
from secrets import token_bytes
from dotenv import load_dotenv
load_dotenv()

# 의사 난수 생성
def generate_pseudo_number():
    master_key = environ.get('MASTER_KEY')
    secret_key = token_bytes(32) # 채팅방 고유 비밀키
    iv = token_bytes(12) # 초기화 벡터 (12 Bytes 권장)

    return master_key, secret_key, iv

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