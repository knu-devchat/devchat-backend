from django.db import models

# Create your models here.
class ChatRoom(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.room_name} ({self.room_id})"

class SecureData(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    encrypted_value = models.TextField() # base64 암호문 저장
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SecureData for room {self.room.room_id} @ {self.created_at.isoformat()}"