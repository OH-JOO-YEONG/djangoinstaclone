from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Profile, Follow
import json
from django.http import HttpResponse

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES) #사인업폼으로부터 받아온 파일과 게시폼
        if form.is_valid(): # 폼의 값이 있다면
            user = form.save() # 폼을 저장
            return redirect('accounts:login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })

def login_check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=name, password=pwd) # 유저가 데이터베이스에 있는지 확인

        if user is not None: #유저가 만약 데이터베이스에 있다면
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'accounts/login_fail.html')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {
            'form': form
        })

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required
@require_POST
def follow(request):
    from_user = request.user.profile
    pk = request.POST.get('pk')
    to_user = get_object_or_404(Profile, pk=pk)
    follow, created = Follow.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        message = '팔로우 시작!'
        status = 1
    else:
        follow.delete()
        message = '팔로우 취소'
        status = 0
    context = {
        'message': message,
        'status': status,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")