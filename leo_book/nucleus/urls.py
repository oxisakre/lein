from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('profile/<str:pk>', views.profile, name='profile'), # str:pk es para el user el pk es el usuario y el str es string
    path('like-post', views.like_post, name='like-post'),
    path('share-post', views.share, name='share-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]