from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from network.forms import NewPostForm
from .models import Post, Follow, User

def index(request):
    posts = Post.objects.order_by("-datetime").all()
    return render(request, 'network/index.html', {
        "title": "All Posts",
        "form": NewPostForm(),
        "posts": posts
    })

def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post(author=request.user, content=content, datetime=datetime.now)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(author=profile_user).all()
    followers = Follow.objects.filter(followed=profile_user).all().count()
    following = Follow.objects.filter(follower=profile_user).all().count()
    (follow, label) = get_following_status(request.user, profile_user)

    return render(request, "network/profile.html", {
                            "username": username,
                            "followers": followers,
                            "following": following,
                            "label": label,
                            "posts": posts
    })

def following(request):
    following = Follow.objects.filter(follower=request.user).all()
    
    posts = [f.followed.posts.order_by("-datetime").all() for f in following]
    return render(request, 'network/index.html', {
        "title": "Following",
        "posts": posts
    })

def follow_unfollow(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(author=profile_user).all()
    followers = Follow.objects.filter(followed=profile_user).all().count()
    following = Follow.objects.filter(follower=profile_user).all().count()
    (follow, label) = get_following_status(request.user, profile_user)

    if follow != None:
        follow.delete()
        label = "Follow"
    else:
        follow = Follow(follower=request.user, followed=profile_user)
        follow.save()
        label = "Unfollow"

    return render(request, "network/profile.html", {
                            "username": username,
                            "followers": followers,
                            "following": following,
                            "label": label,
                            "posts": posts
    })

def get_following_status(follower, followed):
    try:
        follow = Follow.objects.get(follower=follower, followed=followed)
        label = "Unfollow"
    except:
        follow = None
        label = "Follow"
    return (follow, label)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
