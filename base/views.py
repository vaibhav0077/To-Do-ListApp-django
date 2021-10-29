from typing import ValuesView
from django.db.models import query
from django.db.models.query_utils import Q
from django.http import request, FileResponse, response, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import html
from reportlab.lib import pagesizes
from reportlab.lib.utils import fileName2FSEnc
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from base.models import TODO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from .tables import TODOTable
import csv
from django_tables2 import RequestConfig
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# History Task
def history(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        # form = TODOForm()
        totos = TODO.objects.filter(user=user, status="C").order_by('title')

        # table = TODOTable(TODO.objects.filter(
        #     user=user).order_by('title'))
        # variabe_name = TableName(model_name.objects.filter(user=user).order_by())
        # c_task = TODOTable(user.objects.get(status = "C"))
        table = TODOTable(TODO.objects.filter(
            user=user, status="C").order_by('title'))

        # print('=======================================Tabletable ', table)

        return render(request, "base/history.html", context={'table': table, 'totos': totos})

    else:
        # form = AuthenticationForm(request)
        # return render(request, 'base/login.html', context={'form': form})
        return redirect('/login')

# Generate CSV file


def csv_generate(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Title', 'Status', 'Priority', 'Start Date', 'End date'])
    user = request.user
    for data in TODO.objects.filter(user=user).values_list('title', 'status', 'priority', 'date', 'end_date'):
        writer.writerow(data)

    response['Content-Disposition'] = 'attachment; filename = "tasks.csv" '

    return response


# Generate pdf file
def pdf_generate(request):
    # Create Byte stream Buffer
    buf = io.BytesIO()
    # create Canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create Text Object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add Some Lines TExt

    lines = []
    # lines = []
    if request.user.is_authenticated:
        user = request.user
        view_todos = TODO.objects.filter(user=user)
        # print(view_todos)
        # date = view_todos.date
        # form = TODOForm(instance=view_todos)
        # return render(request, 'base/taskViewing.html', {"date": date})

    for v in view_todos:
        # d = v.end_date
        # print(d.day)
        lines.append(f"Title : { v.title} ")
        lines.append(f"Status  :{v.status} ")
        lines.append(f"Priority : {v.priority}")
        lines.append(f"Start Date : {str(v.date)} ")
        lines.append(f"End Date : {str(v.end_date)}")
        lines.append("=========================")

    # print(lines)
    # Loop
    textob.textLine(user.username)
    textob.textLine(
        "---------------------------------------------------------------------------------------------------------")
    for line in lines:
        textob.textLine(line)

    # Finish Up

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # return Something

    return FileResponse(buf, as_attachment=True, filename="report.pdf")


def show_mymodels(request):
    table = TODOTable(TODO.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'base/index_django.html', {'table': table})


def index_django(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user, status="P").order_by('priority')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(
            user=user, status="P").order_by('priority'))
        # totoTODO.objects.filter(user=user, status = "C").order_by('title')
        # variabe_name = TableName(model_name.objects.filter(user=user).order_by())

        # print('Tabletable ', table)

        return render(request, "base/index_django.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        # form = AuthenticationForm(request)
        # return render(request, 'base/login.html', context={'form': form})
        return redirect('/login')


def index(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('end_date', 'priority')
        for t in totos:
            due_date_for_task = t.end_date.day - date.today().day
            # print(str(t.pk) + "==== " + str(due_date_for_task))
            due_date_dict[t.pk] = due_date_for_task

        return render(request, 'base/index.html', context={'form': form, 'totos': totos, 'due_date_dict': due_date_dict, })
    else:
        # form = AuthenticationForm(request)
        # return render(request, 'base/login.html', context={'form': form})
        return redirect('/login')


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
            messages.error(request, 'Please Enter Valid Data')
            return render(request, 'base/signup.html', {'form': fm})

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
                # print("=========================================================")
                return redirect("/home")
                # return render(request, 'base/home.html')

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        fm = AuthenticationForm()
        messages.error(request, "Login the Form")
    return render(request, 'base/login.html', {'form': fm})


def home(request):
    return render(request, 'base/home.html')


def add_todo(request):

    if request.user.is_authenticated:
        user = request.user
        # print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()

            return redirect("/home")

        else:
            messages.info(request, 'Values Are Invalid , No Task Is Added')
            return redirect("/home")


def signout(request):
    logout(request)
    return render(request, 'base/logout.html')


def delete_todo(request, id):
    # print(id)
    TODO.objects.get(pk=id).delete()
    return redirect(request.META.get('HTTP_REFERER'))


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect("/home")


def edit_task(request, id):
    todo = TODO.objects.get(pk=id)
    form = viewTodoForm(instance=todo)

    if request.method == "POST":
        form = viewTodoForm(request.POST, instance=todo)
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
        return redirect('/login')


def view_todo(request, id):
    if request.user.is_authenticated:
        view_todos = TODO.objects.get(pk=id)
        # print(view_todos)
        date = view_todos.date

        form = TODOForm(instance=view_todos)
        return render(request, 'base/taskViewing.html', {'form': form, "date": date})


def search_query(request):
    if request.user.is_authenticated:
        user = request.user
        query = request.GET['query']
        print(type(query), "query=====")
        print(query)
        if len(query) != 0:
            view_todos = TODO.objects.filter(Q(title__icontains=query) | Q(status__icontains=query) | Q(
                date__icontains=str(query)) | Q(end_date__icontains=str(query)) | Q(priority__icontains=query))
            table = TODOTable(TODO.objects.filter(Q(title__icontains=query) | Q(status__icontains=query) | Q(
                date__icontains=str(query)) | Q(end_date__icontains=str(query)) | Q(priority__icontains=query), user=user))
            return render(request, 'base/search.html', {'table': table, 'view_todos': view_todos, 'query': query})
        else:
            print("Nothing")
            messages.error(request, "Please enter Something in Search Box")
            return redirect('/home')


def search_query_title_as(request):
    if request.user.is_authenticated:
        due_date_dict = {}
        user = request.user
        form = TODOForm()
        totos = TODO.objects.filter(user=user).order_by('priority', 'end')
        # for t in totos:
        # due_date_for_task = t.end_date.day - date.today().day
        # print(str(t.pk) + "==== " + str(due_date_for_task))
        # due_date_dict[t.pk] = due_date_for_task
        table = TODOTable(TODO.objects.filter(user=user).order_by('priority'))
        # variabe_name = TableName(model_name.objects.filter(user=user).order_by())

        print('Tabletable ', table)

        return render(request, "base/index_django.html", context={'form': form, 'table': table, 'totos': totos, 'due_date_dict': due_date_dict, })

    else:
        # form = AuthenticationForm(request)
        # return render(request, 'base/login.html', context={'form': form})
        return redirect('/login')


def search_query_title_ds(request):
    if request.user.is_authenticated:
        user = request.user
        # print("sdddddssssssss")
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
        # print("sdddddssssssss")
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
        # print("sdddddssssssss")
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
        # print("sdddddssssssss")
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
            # print(user.password)
            curpass = request.POST.get('currentPassword')
            password1 = request.POST.get('newPassword')
            password2 = request.POST.get('confirmPassword')
            # print("password1 : ", curpass)
            if user.check_password(curpass):
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(request, "Password Changed")
                    return redirect('/login')

                else:
                    messages.error(request, "Password Does Not Match")
                    change_pass = changePassForm()
                    return render(request, 'base/changePass.html', {'change_pass': change_pass})
            else:
                messages.error(request, "Incorrect current Password")
                change_pass = changePassForm()
                return render(request, 'base/changePass.html', {'change_pass': change_pass})

        else:
            change_pass = changePassForm()
            return render(request, 'base/changePass.html', {'change_pass': change_pass})

    else:
        return render(request, 'base/login.html')


def task_details(request, task_id):
    if request.session.has_key('username'):
        login_user = request.session["username"]
        login_user_obj = UserRegister.objects.get(username=login_user)
        # print(task_id)
        task_obj = get_object_or_404(TaskData, pk=task_id)
        content = {"login_user_obj": login_user_obj, 'tash_obj': task_obj}
        return render(request, 'app/task_details.html', content)
    else:
        return redirect('user-login')
