from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import WorkingTimeModel
from .forms import WorkingForm

import datetime


# INDEX トップページ
def index(request):
    params = {
        "page_title": "トップ / 退勤管理アプリ",
        "user": request.user,
    }
    
    return render(request, "index.html", params)


# SIGNUP 従業員登録ページ
def signupFunc(request):
    params = {
        "page_title": "従業員登録 / 退勤管理アプリ",
        "user": request.user,
    }
    
    if request.method == "GET":
        return render(request, "signup.html", params)
    else:
        print(request.POST)
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        
        if password != password_confirm:
            params["error"] = "パスワードが異なっています。入力しなおしてください"
            return render(request, "signup.html", params)
        
        if first_name == "":
            params["error"] = "姓を正しく入力してください"
            return render(request, "signup.html", params)
        
        if last_name == "":
            params["error"] = "名を正しく入力してください"
            return render(request, "signup.html", params)
        
        
        try:
            user = User.objects.create_user(username, "", password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except ValueError:
            params["error"] = "入力欄にログインID、姓名、パスワードをしっかりと入力してください"
            return render(request, "signup.html", params)
        except IntegrityError:
            params["error"] = "既に登録されているユーザーです。ログインページからログインしてください。"
            return render(request, "signup.html", params)
        
        return redirect("login")


# LOGIN ログインページ(従業員・管理者共通)
def loginFunc(request):
    params = {
        "page_title": "ログイン / 退勤管理アプリ",
        "user": request.user,
    }
    
    if request.method == "GET":
        if request.user.is_authenticated:
            params["error"] = f"既に{request.user.username}でログインしています。"
            return render(request, "index.html", params)
        return render(request, "login.html", params)
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            params["message"] = f"{username}でログインしました。"
            return render(request, "index.html", params) ###後で従業員ごとの労働情報追加ページに変更
        else:
            params["error"] = "ログインに失敗しました。ログインIDとパスワードを確認してください。"
            return render(request, "login.html", params)


# LOGOUT ログアウト(従業員・管理者共通)
@login_required
def logoutFunc(request):
    logout(request)
    return redirect("index")


# 従業員情報ページ(個人ページ)
@login_required
def workerInfoFunc(request, id):
    params = {
        "page_title": f"{request.user.first_name + request.user.last_name}さんのページ / 退勤管理アプリ",
        "user": request.user,
        "workings": WorkingTimeModel.objects.filter(worker=request.user.pk)
    }
    
    if request.user.username == "admin":
        params["user"] = User.objects.filter(pk=id)
    
    if request.method == "GET":
        return render(request, "worker_info.html", params)
    else:
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user = request.user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
        
        return render(request, "worker_info.html", params)


@login_required
def addWorkingInfoFunc(request):
    params = {
        "page_title": "退勤情報追加 / 退勤管理アプリ",
        "user": request.user,
        "form": WorkingForm(),
        "workings": WorkingTimeModel.objects.filter(worker=request.user.pk)
    }
    work_times = datetime.timedelta(minutes=0)
    for working in params["workings"]:
        work_times += working.work_time
    params["work_times"] = work_times
    
    if request.method == "GET":
        return render(request, "worker/add_working_info.html", params)
    else:
        worker = request.user.pk
        start = request.POST["start"]
        finish = request.POST["finish"]
        working = WorkingTimeModel(worker=worker, start=start, finish=finish)
        start_dt = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        finish_dt = datetime.datetime.strptime(finish, '%Y-%m-%d %H:%M:%S')
        working_time = abs(start_dt - finish_dt)
        working.work_time += working_time
        print(worker, start, finish, working_time)
        working.save()
        
        return render(request, "worker/add_working_info.html", params)


@login_required
def workerListFunc(request):
    params = {
        "page_title": "従業員リスト / 退勤管理アプリ",
        "user": request.user,
        "objects": User.objects.all()
    }
    
    if request.user.username != "admin":
        params["error"] = "このページへのアクセスは制限されています。"
        return redirect("index", params)
    
    return render(request, "admin/worker_list.html", params)


@login_required
def adminWorkerInfoFunc(request, id):
    params = {
        "page_title": "従業員情報 / 退勤管理アプリ",
        "user": request.user,
        "worker": User.objects.filter(pk=id),
    }
    
    if request.user.username != "admin":
        params["error"] = "このページへのアクセスは制限されています。"
        return redirect("index", params)
    
    return render(request, "admin/worker_info.html", params)


@login_required
def deleteWorkerFunc(request, id):
    worker = User.objects.filter(pk=id)
    worker.delete()
    return redirect("workerList")
