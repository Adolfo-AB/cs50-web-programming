from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from itertools import chain

from network.forms import NewPostForm
from .models import Post, Follow, User

def index(request):
    posts = Post.objects.order_by("-datetime").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, 'network/index.html', {
        "title": "All Posts",
        "form": NewPostForm(),
        "page_posts": page_posts
    })

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post(author=request.user, content=content, datetime=datetime.now)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    profile_user = User.objects.get(username=username)
    posts = Post.objects.filter(author=profile_user).order_by("-datetime").all()
    followers = Follow.objects.filter(followed=profile_user).all().count()
    following = Follow.objects.filter(follower=profile_user).all().count()
    (follow, label) = get_following_status(request.user, profile_user)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
                            "username": username,
                            "followers": followers,
                            "following": following,
                            "label": label,
                            "page_posts": page_posts
    })

def following(request):
    followed_users = [f.followed for f in Follow.objects.filter(follower=request.user).all()]
    posts = [Post.objects.filter(author=user).all() for user in followed_users]
    posts = list(chain(*posts))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, 'network/index.html', {
        "title": "Following",
        "page_posts": page_posts
    })

@login_required
def follow_unfollow(request, username):
    if request.user.username != username:
        profile_user = User.objects.get(username=username)
        posts = Post.objects.filter(author=profile_user).all()
        (follow, label) = get_following_status(request.user, profile_user)

        if follow != None:
            follow.delete()
            label = "Follow"
        else:
            follow = Follow(follower=request.user, followed=profile_user)
            follow.save()
            label = "Unfollow"

        followers = Follow.objects.filter(followed=profile_user).all().count()
        following = Follow.objects.filter(follower=profile_user).all().count()

        return render(request, "network/profile.html", {
                                "username": username,
                                "followers": followers,
                                "following": following,
                                "label": label,
                                "posts": posts
        })
    else:
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

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
