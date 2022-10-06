import email
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages

from nucleus.models import Profile
# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
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
                # crear un perfil para el usuario nuevo
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
    else:    
        return render(request, 'signup.html')