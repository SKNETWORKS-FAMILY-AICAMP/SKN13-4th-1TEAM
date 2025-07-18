from django.db import models
from django.contrib.auth.models import User  # ✅ 이거 추가해야 User 외래키 연결됨

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 누가 만든 쪽지함인지
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:30]}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_announcement = models.BooleanField(default=False) # 공지 여부 필드 추가
    is_anonymous = models.BooleanField(default=False) # 익명 여부 필드 추가

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments_made') # 추가된 user 필드
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') # 대댓글을 위한 부모 댓글 필드
    author_name = models.CharField(max_length=50) # 기존 author_name 유지
    password = models.CharField(max_length=128) # 비밀번호 해싱을 위해 128자로 설정
    content = models.TextField()
    is_deleted_by_admin = models.BooleanField(default=False) # 관리자 삭제 여부 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'

    class Meta:
        ordering = ['created_at'] # 대댓글은 템플릿에서 계층적으로 정렬


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'

    class Meta:
        ordering = ['-created_at']
