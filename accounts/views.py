from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'food:randreci')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect("food:randreci")

def user_page(request, id):
    user_info = get_object_or_404(User, id=id)
    
    # 하고있는거
    # total = user_info.followings.all()
    # 당하는거
    # total2 = user_info.followers.all()
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)

def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user
    # 내가 나를 팔로우할 수 없도록
    if you != me:
        if you in me.followings.all():
            me.followings.remove(you)
            # you.followers.remove(me)
        else:
            me.followings.add(you)
            # you.followers.add(me)
    return redirect('accounts:user_page', id)

def delete(request, id):
    user_info = get_object_or_404(User, id=id)
    user = request.user
    # 로그인한 유저인 경우(조건이 없어도 되지만 확인차 작성)
    if user == user_info:
        user.delete()
    return redirect('posts:index')

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 비밀번호 변경 후 로그인 유지
            update_session_auth_hash(request, user)
            return redirect('posts:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

# allauth로 로그인후 돌아가는 경로
def profile(request):
    user_info = request.user
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/user_page.html', context)
