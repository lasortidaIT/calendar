from django.contrib import admin
from django.urls import path
from main.views import base_view, delete_event
from loging.views import login_view, register_view, verify_view, logout_view

# указываем обработчик для каждого запроса
urlpatterns = [
    path('admin/', admin.site.urls), # админка
    path('', base_view), # главная страница
    path('login/', login_view), # вход в аккаунт
    path('register/', register_view), # регистрация
    path('verify/<str:uuid>/', verify_view), # подтверждение аккаунта с параметром uuid
    path('logout/', logout_view), # выход из аккаунта
    path('delete/event/<str:id>/', delete_event)
]

