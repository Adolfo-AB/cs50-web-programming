import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse


from .models import User, Post, UserProfile


def index(request):
    return render(request, "network/index.html")

@login_required
def save_post(request):
    if request.method == "POST":
        form = Post(content=request.POST['content'])
        form.author = UserProfile.objects.get(user=request.user)
        form.save()
    elif request.method == "PUT":
        content = json.loads(request.body)
        post_id = int(content["post_id"])
        new_content = content["new_content"]
        post = Post.objects.filter(id=post_id).first()

        if post.author.user != request.user:
            return HttpResponse(status=401)
        
        post.content = new_content
        post.save()

        return JsonResponse({
            "result": True
        }, status=200)

    else:
        return JsonResponse({
            "error": f"Invalid request"
        }, status=400)
    return index(request)

@login_required
def update_follow(request, profile_id):
    profile = UserProfile.objects.get(id=profile_id)

    if profile in request.user.get_following.all():
        new_status = False
        profile.followers.remove(request.user)
    else:
        new_status = True
        profile.followers.add(request.user)
        
    profile.save()
    return JsonResponse({"newFollower": new_status, "newAmount": profile.followers.count()}, status=200)

@login_required
def update_like(request, post_id):
    profile = UserProfile.objects.filter(user=request.user).first()
    post = Post.objects.get(id=post_id)

    if post in profile.get_likes.all():
        new_status = False
        post.likes.remove(profile)
    else:
        new_status = True
        post.likes.add(profile)
        
    post.save()
    return JsonResponse({"liked": new_status, "newAmount": post.likes.count()}, status=200)

@login_required
def load_following(request):
    following_profiles = request.user.get_following.all()
    posts = Post.objects.filter(author__in=following_profiles).all()
    return paginate(request, posts)

def load(request):
    user_profile = request.GET.get("profile", None)
    if (user_profile):
        posts = Post.objects.filter(author=user_profile).all()
    else:
        posts = Post.objects.all()
    return paginate(request, posts)

def paginate(request, posts):
    posts = posts.order_by("datetime").all()

    paginator = Paginator(posts, 10)
    page = paginator.get_page(request.GET["page"])
    return JsonResponse({
        "posts": [post.serialize(request.user) for post in page],
        "num_pages": paginator.num_pages
    },
    safe = False)

def profile(request, user_id):
    user_profile = UserProfile.objects.filter(id=user_id).first()
    return JsonResponse(user_profile.serialize(request.user), status=200)

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
        userProfile = UserProfile(user=user)
        userProfile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
