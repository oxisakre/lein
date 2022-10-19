from dataclasses import asdict
import email
from email.mime import image
from multiprocessing import AuthenticationError
from socket import AF_IRDA
from sunau import AUDIO_FILE_ENCODING_FLOAT
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required # hacer que el usuario se tenga que logear
from requests import request
from nucleus.models import Post 

from nucleus.models import Profile
# Create your views here.

@login_required(login_url='signin') # para que el usuario tenga que logearse, lo va a mandar siempre al signin
def index(request):
    user_object = User.objects.get(username=request.user.username) # para obetener el objeto del usuario conectado- user sirve porque es la foreingkey
    user_profile = Profile.objects.get(user=user_object) # para obtener el perfil del usuario

    posts = Post.objects.all() # devuelve una lista 
    return render(request, 'index.html', {'user_profile' : user_profile, 'posts' : posts}) # para pasarle el userprofile al html

@login_required(login_url='signin')
def upload(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profimg  = user_profile.profileimg
        user = request.user.username
        image = request.FILES.get('image_upload') # porque en el index el input se llama image_upload
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, profimg=profimg, image=image, caption=caption)
        new_post.save
        
        return redirect('/')
    else:
        return redirect('/')

def like_post(request):
    pass   

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user) # lo que hace es que si get(obtiene) el objeto 'user'

    if request.method == 'POST':
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                full_name = request.POST['full_name']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.full_name = full_name
                user_profile.save()
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                full_name = request.POST['full_name']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.full_name = full_name
                user_profile.save()
            return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username'] #devuelve el username
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2: #chequear datos
            if User.objects.filter(email=email).exists(): 
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password) #crea el usuario
                user.save()

                #logear al usuario y redirigirlo a la pagina de configuracion
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # crear un perfil para el usuario nuevo
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
    else:    
        return render(request, 'signup.html')

def signin(request):

    if request.user.is_authenticated:
        return redirect('/')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')