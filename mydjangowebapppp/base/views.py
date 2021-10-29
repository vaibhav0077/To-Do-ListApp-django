# from To_Do_List.base.models import TODO
# from To_Do_List import base
from django.db.models import query
from django.http import request
from django.shortcuts import render, redirect
from django.utils import html
# from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from base.models import TODO
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/base/login')


def index(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def sign_up(request):
    if request.method == 'POST':
        fm = SignUpform(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account Created Successfully')
            fm.save()
            # return render(request, 'base/login.html')
            # return render(request, 'base/home.html')
            return redirect('/login')

    else:
        fm = SignUpform()
    return render(request, 'base/signup.html', {'form': fm})


def login_request(request):
    if request.method == "POST":
        fm = AuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/home")
                # return render(request, 'base/home.html')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    fm = AuthenticationForm()
    return render(request, 'base/login.html', {'form': fm})


def home(request):
    return render(request, 'base/home.html')


def add_todo(request):

    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            # return render(request,'base\index.html')
            return redirect("/home")

        else:
            form = TODOForm()
            return render(request, 'base\index.html', context={'form': form})


def signout(request):
    logout(request)
    return render(request, 'base/home.html')


def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect("/home")


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect("/home")


def edit_task(request, id):
    todo = TODO.objects.get(pk=id)
    form = TODOForm(instance=todo)

    if request.method == "POST":
        form = TODOForm(request.POST, instance=todo)
        title_task = TODO.objects.get(pk=id)
        if form.is_valid():
            form.save()
            messages.info(request, f"{title_task.title} is updated")
            title_task = TODO.objects.get(pk=id)
            # messages.info(request, f"to {title_task.title} ")
            return redirect("/home")

    return render(request, 'base/edit.html', {'form': form})


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            prof_edit = UserUpdateForm(request.POST, instance=request.user)
            if prof_edit.is_valid():
                prof_edit.save()
                messages.success(request, 'profile Edit Successfully')
            else:
                messages.error(request, 'Enter all Details Properly')
                prof_edit = UserUpdateForm(instance=request.user)

        prof_edit = UserUpdateForm(instance=request.user)

        return render(request, 'base/profile.html', {'name': request.user.username, 'form': prof_edit})
    else:
        return render(request, 'base/login.html')


def view_todo(request, id):
    if request.user.is_authenticated:
        view_todos = TODO.objects.get(pk=id)
        print(view_todos)
        date = view_todos.date
        # print(view_todo.cleaned_data['date'])
        # print (view_todos['date'].value())
        # print(view_todos.instance.id)
        form = TODOForm(instance=view_todos)
        return render(request, 'base/taskViewing.html', {'form': form, "date": date})


def search_query(request):
    if request.user.is_authenticated:
        query = request.GET['query']
        view_todos = TODO.objects.filter(title__icontains=query)
        return render(request, 'base/search.html', {'view_todos': view_todos, 'query': query})


def search_query_title_as(request):
    if request.user.is_authenticated:
        user = request.user
        print("aasssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('title')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def search_query_title_ds(request):
    if request.user.is_authenticated:
        user = request.user
        print("sdddddssssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('-title')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def search_query_status_as(request):
    if request.user.is_authenticated:
        user = request.user
        print("sdddddssssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('status')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def search_query_status_ds(request):
    if request.user.is_authenticated:
        user = request.user
        print("sdddddssssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('-status')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def search_query_priority_as(request):
    if request.user.is_authenticated:
        user = request.user
        print("sdddddssssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def search_query_priority_ds(request):

    if request.user.is_authenticated:
        user = request.user
        print("sdddddssssssss")
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('-priority')
        return render(request, 'base/index.html', context={
            'form': form,
            'totos': totos
        })
    else:
        return render(request, 'base/home.html')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            # change_pass = changePassForm(request.POST, instance=request.user)
            # return render(request, 'base/changePass.html',{'change_pass':change_pass})
            print(user.password)
            curpass = request.POST.get('currentPassword')
            password1 = request.POST.get('newPassword')
            password2 = request.POST.get('confirmPassword')
            print("password1 : ",curpass)
            if user.check_password(curpass):
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, "Password Changed")
                    return redirect('/login')
                    
                else:
                    messages.error(request, "Password Does Not Match")
                    change_pass = changePassForm()
                    return render(request, 'base/changePass.html', {'change_pass': change_pass} )
            else:
                messages.error(request, "Incorrect current Password")
                change_pass=changePassForm()
                return render(request, 'base/changePass.html', {'change_pass': change_pass} )

        else:
            change_pass=changePassForm()
            return render(request, 'base/changePass.html', {'change_pass': change_pass})

    else:
        return render(request, 'base/login.html')


