from django.db import models

# Create your models here.
class SecureData(models.Model):
    chat_id = models.IntegerField()
    chat_name = models.CharField(max_length=20)
    encrypted_value = models.TextField() # base64 암호문 저장
    created_at = models.DateTimeField(auto_now_add=True)