from django.shortcuts import render, redirect
from .models import Profile, Post
from django.contrib import messages
from .forms import PostForm


def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Your Post Send Success !!!"))
                return redirect('home')

        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'posts': posts, 'form': form})
    else:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'posts': posts})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You Must Be Logged In !!!"))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html', {'profile': profile, "posts": posts})
    else:
        messages.success(request, ("You Must Be Logged In !!!"))
        return redirect('home')
