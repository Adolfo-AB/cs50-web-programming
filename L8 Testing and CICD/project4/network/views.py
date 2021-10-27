import json
from itertools import chain
from datetime import datetime as dtime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def add(request):
    # Adding a new post must be via POST method
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get new post content, author and datetime
    data = json.loads(request.body)
    content = data.get("content", "")
    datetime = dtime.now()
    author = request.user

    post = Post(author=author, datetime=datetime, content=content)
    post.save()

    return JsonResponse({"message": "Post saved successfully."}, status=201)

@csrf_exempt
def load(request, page):
    # Filter emails returned based on page
    if page == "all":
        posts = Post.objects.order_by("-datetime").all()
    elif page == "following":
        followed_users = [f.followed for f in Follow.objects.filter(follower=request.user).all()]
        posts = [Post.objects.filter(author=user).all() for user in followed_users]
        posts = list(chain(*posts))
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
def load_profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        return JsonResponse({"error": "Invalid profile."})

    posts = Post.objects.filter(author=profile_user).order_by("-datetime").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
def update_follow_status(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        return JsonResponse({"error": "Invalid profile."})
    
    follow = Follow.objects.filter(follower=request.user, followed=profile_user).first()
    print(follow)
    if follow != None:
        follow.delete()
        return JsonResponse({"message": "Unfollow successful."}, safe=False)
    else:
        follow = Follow(follower=request.user, followed=profile_user)
        follow.save()
        return JsonResponse(follow.serialize(), safe=False)

@csrf_exempt
def get_follow_status(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        return JsonResponse({"error": "Invalid profile."})
    
    follow = Follow.objects.filter(follower=request.user, followed=profile_user).first()

    if follow == None:
        return JsonResponse({"message": "Not following."})
    else:
        return JsonResponse(follow.serialize(), safe=False)


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
