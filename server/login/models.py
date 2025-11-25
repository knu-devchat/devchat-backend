from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # GitHub 관련 정보
    github_avatar_url = models.URLField(blank=True, null=True)
    github_id = models.CharField(max_length=50, blank=True, null=True)
    
    # 프로필 정보
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # 채팅 설정
    notification_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class RoomAccess(models.Model):
    """방 입장 기록 및 TOTP 검증 상태"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.IntegerField()  # ChatRoom의 room_id와 연결
    
    # 입장 상태
    is_totp_verified = models.BooleanField(default=False)
    entered_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # 세션 관리
    session_key = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'room_id']
    
    def __str__(self):
        return f"{self.user.username} access to room {self.room_id}"
    
    @property
    def chat_room(self):
        """기존 ChatRoom 모델과 연결"""
        from chat.models import ChatRoom
        try:
            return ChatRoom.objects.get(room_id=self.room_id)
        except ChatRoom.DoesNotExist:
            return None

class Message(models.Model):
    """채팅 메시지 모델"""
    room_id = models.IntegerField()  # ChatRoom의 room_id와 연결
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # 메시지 내용
    encrypted_content = models.TextField()  # 암호화된 메시지만 저장
    
    # 메시지 타입
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
        ('system', 'System'),  # 입장/퇴장 알림 등
    ]
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    
    # 타임스탬프
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    # 메시지 상태
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.author.username} in room {self.room_id}: [encrypted message]"
    
    @property
    def chat_room(self):
        """기존 ChatRoom 모델과 연결"""
        from chat.models import ChatRoom
        try:
            return ChatRoom.objects.get(room_id=self.room_id)
        except ChatRoom.DoesNotExist:
            return None

# User 생성 시 자동으로 UserProfile 생성
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)