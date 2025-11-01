from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from random import randint
from django.core.mail import send_mail
from django.conf import settings


def custom_render(request, name, mobile='', context={}):
    return render(request, f'{mobile}/{name}', context)

# обработчик входа в аккаунт
def login_view(request):
    mobile = 'mobile/' if "Mobile" in request.headers["User-Agent"] else ''
    if request.method == 'POST': # если нажимается кнопка в форме
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None: # если пользователь правильно всё ввёл
            login(request, user)
            return redirect('../') # перенаправляем на главную страницу
        else:
            # пользователь с такими данными не найден
            context = {'error': 'Неверные данные для входа!'}
            return render(request, f'{mobile}login-panel.html', context)

    return render(request, f'{mobile}login-panel.html')


# обработчик регистрации аккаунта
def register_view(request):
    mobile = 'mobile/' if "Mobile" in request.headers["User-Agent"] else ''
    if request.method == 'POST': # если нажимается кнопка в форме
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        timezone_str = request.POST.get("timezone") or 'UTC'

        if password != password2:
            context = {'error': 'Пароли не совпадают!'}
            return render(request, f'{mobile}register-panel.html', context)

        if CustomUser.objects.filter(email=email).exists():
            context = {'error': 'Адрес электронной почты уже используется!'}
            return render(request, f'{mobile}register-panel.html', context)

        token = str(randint(100000, 999999)) # создаём код подтверждения
        user = CustomUser.objects.create_user(email=email, password=password, token=token, timezone=timezone_str)
        login(request, user)
        send_mail(
            subject='Код подтверждения календаря',
            message=f"Здравствуйте! Ваш код подтверждения: {token}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return redirect(f'/verify/{str(user.uuid)}') # перенаправляем на страницу подтверждения
    return render(request, f'{mobile}register-panel.html')

# обработчик выхода из аккаунта
def logout_view(request):
    logout(request)
    return redirect('../')

# обработчик подтверждения аккаунта
def verify_view(request, uuid):
    mobile = 'mobile/' if "Mobile" in request.headers["User-Agent"] else ''
    if request.method == 'POST': # если нажимается кнопка в форме
        code = request.POST.get('code')
        if str(code) == str(request.user.token) and request.user.wrong_code_actions < 3: # если код верный
            user = request.user
            user.is_verified = True # аккаунт подтверждён
            user.save() # сохраняем изменения
            return redirect('/')
        user = request.user
        user.wrong_code_actions += 1
        if user.wrong_code_actions >= 3:
            context = {'error': 'Превышено кол-во попыток!'}
        else:
            context = {'error': f'Неверный код! Осталось попыток {3 - user.wrong_code_actions}'}
        user.save()
        return render(request, f'{mobile}verification-page.html', context)
    if (request.method == 'GET' and request.user.is_authenticated
            and str(request.user.uuid) == str(uuid) and not request.user.is_verified): # просто переход на страницу верификации
        return render(request, f'{mobile}verification-page.html')
    # если uuid запрашиваемый не совпадает с uuid пользователя,
    # который делает этот запрос (или акканут уже подтвержден) - то на главную страницу
    return redirect('../')
