from django.contrib import admin
from .models import Followers, Profile, Post, LikePost
# Register your models here.
admin.site.register(Profile) #Para ver el modelo 'Profile' en el admin panel de la pagina
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Followers)