"""To_Do_List URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from To_Do_List.base.views import change_status
from django.contrib import admin

from django.urls import path
from base import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up),
    path('', views.index_django),
    path('login/', views.login_request),
    path('home/', views.index_django),
    path('add-todo/', views.add_todo),
    path('logout/', views.signout),
    path('delete_todo/<int:id>/', views.delete_todo, name='delete_todo'),
    path('change_status/<int:id>/<str:status>', views.change_todo),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),
    path('profile/', views.profile),
    path('view_todo/<int:id>', views.view_todo, name='view_todo'),
    path('search/', views.search_query),
    path('title/as/', views.search_query_title_as),
    path('title/ds/', views.search_query_title_ds),
    path('status/as/', views.search_query_status_as),
    path('status/ds/', views.search_query_status_ds),
    path('priority/as/', views.search_query_priority_as),
    path('priority/ds/', views.search_query_priority_ds),
    path('changePassword/', views.change_password),
    path('forget/', auth_views.PasswordResetView.as_view(
        template_name='base/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='base/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='base/password_reset_Confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='base/password_reset_complete.html'), name='password_reset_complete'),

    path('pdf_generate/', views.pdf_generate, name='pdf_generate'),
    path('csv_generate/', views.csv_generate, name='csv_generate'),
    path('history/', views.history, name='history'),


    path('index_django/', views.index_django)



]
