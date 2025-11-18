import json
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from .models import SecureData, ChatRoom


# POST 요청으로 서버에 room_name 전달
def load_room_name(request):
    try:
        if request.content_type == "application/json":
            payload = json.loads(request.body.decode("utf-8") or "{}")
            room_name = payload.get("room_name")
        else:
            room_name = request.POST.get("room_name")
    except Exception:
        return HttpResponseBadRequest("invalid request body")

    if not room_name or not isinstance(room_name, str):
        return HttpResponseBadRequest("missing or invalid 'room_name'")

    room_name = room_name.strip()[:50]
    return room_name


# DB에 ChatRoom, SecureData 저장
def save_room_secret_key(room_name: str, encrypted: str):
    try:
        with transaction.atomic():
            room = ChatRoom.objects.create(room_name=room_name)
            SecureData.objects.create(room=room, encrypted_value=encrypted)
    except IntegrityError:
        return HttpResponseBadRequest("room_name already exists")
    except Exception:
        return HttpResponseServerError("failed to save room and secret")

    return room