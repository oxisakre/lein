from django.db import models
from django.contrib.auth import get_user_model

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