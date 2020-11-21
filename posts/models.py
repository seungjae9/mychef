from django.db import models
from django.conf import settings
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField


# Create your models here.
class HashTag(models.Model):
    content = models.CharField(max_length=100)

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = ProcessedImageField(
                # null=True, # 필드값 유효성검사할 때 빈값도 가능
                # blank=True, # 모델폼 입력할 때 빈값도 가능
                processors=[ResizeToFill(300,300)], # 비율이 안깨지게(리스트형태)
                format='JPEG',
                options={'quality':90}, # 생략해도 상관없음
                upload_to='media' # 경로
            )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(HashTag, related_name="taged_post")

class Comment(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)