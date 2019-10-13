from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm

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