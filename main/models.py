from django.db import models
from django.contrib.auth.models import User
from django.http import request
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, default="", upload_to = "profile/")
    bio = models.TextField(null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    inst_url = models.CharField(max_length=255, null=True, blank=True)
    vk_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.post_text
    
    def publish(self):
        self.post_date = timezone.now()
        self.save()

class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=False, blank=False, default="")

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

class Comment(models.Model):
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.comment_text
    
    def publish(self):
        self.post_date = timezone.now()
        self.save()