from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required # hacer que el usuario se tenga que logear
from nucleus.models import Post, Profile, LikePost , Followers
from itertools import chain


# Create your views here.

@login_required(login_url='signin') # para que el usuario tenga que logearse, lo va a mandar siempre al signin
def index(request):
    user_object = User.objects.get(username=request.user.username) # para obetener el objeto del usuario conectado- user sirve porque es la foreingkey
    user_profile = Profile.objects.get(user=user_object) # para obtener el perfil del usuario

    user_following_list = []
    feed = []

    user_following = Followers.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_list = Post.objects.filter(user=usernames)
        feed.append(feed_list)

    feed_list = list(chain(*feed))

    posts = Post.objects.all() # devuelve una lista 
    return render(request, 'index.html', {'user_profile' : user_profile, 'posts' : feed_list}) # para pasarle el userprofile al html

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

    
def share(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    share_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if request.method == 'GET':
        username = request.user.username
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        share_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
        
        shared = {
            'post' : post,
            'share_filter' : share_filter
        }
        return render(request, 'post_share.html', shared)
    

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id') #obtener el id del post o sea lo busca en el data base (que esta en el modelo del like)

    post = Post.objects.get(id=post_id) # sabes si el id es la misma de la del post, para corroborar el like de la persona

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first() #filtra los post id con el username conectado | el first es solo para obtener uno solo
    # en cambio si fuese get nos tiraria error porque no hay dato 
    if like_filter == None: # porque le filter nos devuelve el primero y si el primero es none pasa esto
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

def profile(request, pk): #pk es lo que pusimos en el url para identificar al usuario
    user_object = User.objects.get(username=pk) # determinando que pk sea el igual al usuario
    user_profile = Profile.objects.get(user=user_object) # pasamos la data de ese usuario
    user_posts = Post.objects.filter(user=pk) # pasamos la data de ese usuario pero de los post
    user_post_length = len(user_posts) # para ver la cantidad de posts

    follower = request.user.username # la persona que quiere seguirlo
    user = pk

    if Followers.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(Followers.objects.filter(user=pk)) # el pk es porque es el especifico usuario al que se sigue digamos, si fuese user seria el conectado
    user_following = len(Followers.objects.filter(follower=pk))


    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

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