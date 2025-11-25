# myapp/tests.py
from django.test import TestCase
from unittest.mock import patch
from .views import init_chat_room

class InitChatRoomTest(TestCase):

    @patch("myapp.views.encrypt_aes_gcm")
    @patch("myapp.views.token_bytes")
    def test_init_chat_room(self, mock_token_bytes, mock_encrypt):
        # token_bytes가 호출될 때 순서대로 값을 반환하도록 설정
        mock_token_bytes.side_effect = [
            b'master_key_32_bytes___________',  # 첫 번째 호출 (master_key)
            b'secret_key_32_bytes___________',  # 두 번째 호출 (secret_key)
            b'iv_12_bytes'                     # 세 번째 호출 (iv)
        ]

        # encrypt_aes_gcm의 결과도 고정
        mock_encrypt.return_value = b'encrypted_ciphertext'

        result = init_chat_room()

        # 기대한 암호문인지 확인
        self.assertEqual(result, b'encrypted_ciphertext')

        # encrypt_aes_gcm이 올바른 매개변수로 호출되었는지 테스트
        mock_encrypt.assert_called_once_with(
            b'master_key_32_bytes___________',
            b'secret_key_32_bytes___________',
            b'iv_12_bytes'
        )
