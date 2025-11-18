from secrets import token_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import environ
from dotenv import load_dotenv
import pyotp
from django.shortcuts import render

load_dotenv()

# Create your views here.
def init_chat_room():
    """
    채팅방 생성 클릭 시 채팅방 고유 비밀키 생성
    """
    master_key = environ.get('MASTER_KEY')
    secret_key = token_bytes(32) # 채팅방 고유 비밀키
    iv = token_bytes(12) # 초기화 벡터 (12 Bytes 권장)

    ciphertext = encrypt_aes_gcm(master_key, secret_key, iv) # AES-GCM 암호화
    # ciphertext를 DB에 저장

    print(f"cipher: {ciphertext}")


def generate_TOTP():
    """
    채팅방 고유 비밀키로 TOTP 생성
    """
    pass

def create_chat_room():
    """
    채팅방 생성 완료. 채팅방에 대한 정보가 DB에 저장됨.
    """
    pass

# AES-GCM 암호화 함수
def encrypt_aes_gcm(master_key: bytes, plaintext: bytes, iv: bytes):
    aesgcm = AESGCM(master_key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return ciphertext