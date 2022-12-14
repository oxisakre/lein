from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
import uuid # para general id unicas
from datetime import datetime

User = get_user_model()
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # usamos el User como foreingkey
    id_user = models.IntegerField()
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='generic-profile_0.png') #el upload genera una carpeta automatica si no la hay
    location = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username 
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) # dar una id unica , hacerlo True cambia la id que da original django y le pone una unica
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    profimg = models.ImageField(upload_to='profile_images')
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
