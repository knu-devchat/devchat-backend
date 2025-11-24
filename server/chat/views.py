import pyotp
from .crypto_utils import encrypt_aes_gcm, decrypt_aes_gcm, generate_pseudo_number
from .utils import load_room_name, save_room_secret_key, get_room_secret
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

@require_POST
def create_chat_room(request):
    """
    req: room_name 전달
    res: room_id, room_name 반환
    """
    try:
        room_name = load_room_name(request)
        if not room_name:
            return JsonResponse({"success": False, "error": "room_name not provided"}, status=400)

        secret_key, iv = generate_pseudo_number()
        encrypted = encrypt_aes_gcm(secret_key, iv)

        room_or_resp = save_room_secret_key(room_name, encrypted)
        if hasattr(room_or_resp, "status_code"):
            return room_or_resp  # 에러 HttpResponse 그대로 반환

        room = room_or_resp
        return JsonResponse({"success": True, "room_id": room.room_id, "room_name": room.room_name})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_GET
def generate_access_totp(request, room_id):
    """
    req: 채팅방 입장 시 프론트가 요청
    res: 6자리 코드 반환 + interval
    """
    try:
        encrypted = get_room_secret(room_id)
        if encrypted is None:
            return JsonResponse({"success": False, "error": "room not found"}, status=404)

        secret = decrypt_aes_gcm(encrypted)
        if not secret:
            return JsonResponse({"success": False, "error": "secret decrypt fail"}, status=500)

        totp = pyotp.TOTP(secret, interval=30)
        code = totp.now()

        return JsonResponse({"success": True, "totp": code, "interval": 30})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)