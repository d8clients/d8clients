from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import LoginForm, UserRegistrationForm, PasswordChangeForm, UserChangeForm
from client.models import Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


def main(request):
    # главная страница веб-приложения
    return render(request, 'base/main.html')


def about_us(request):
    # страница с информацией о проекте
    return render(request, 'base/about_us.html')


def registration_page(request):
    """
        регистрация нового пользователя
        с помощью формы UserRegistrationForm()
    """
    if request.user.is_authenticated:
        return redirect('client_profile')

    form = UserRegistrationForm()
    next_url = request.GET.get('next') if 'next' in request.GET else 'client_profile'

    # если пользователь отправил форму
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        # если форма заполнена корректно, то создаем нового пользователя, иначе выводим ошибку
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # создаем объект client, если пользователь хочет клиентский функционал
            if user.is_client:
                client = Client(user=user)
                client.save()
            # происходит авторизация пользователя и перенаправление
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Произошла ошибка во время регистрации, попробуйте еще раз')

    context = {'form': form, 'next_url': next_url}
    return render(request, 'base/registration_page.html', context=context)


def login_page(request):
    """
        аутентификация и авторизация пользователя
        по email и паролю
    """
    # если пользователь уже авторизован, то перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('client_profile')

    form = LoginForm()
    next_url = request.GET.get('next') if 'next' in request.GET else 'client_profile'

    if request.method == "POST":

        form = LoginForm(request.POST)

        # если пользователь корректно ввел форму, пытаемся авторизовать его
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])

            # если пользователь с такими данными нашелся, смотрим, есть ли у него доступ к сайту
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(next_url)
                else:
                    messages.error(request, 'Неактивный аккаунт')
            else:
                messages.error(request, 'Неверный e-mail или пароль')

    context = {'form': form, 'next_url': next_url}
    return render(request, 'base/login_page.html', context=context)


def logout_page(request):
    """
        выход пользователя из аккаунта
    """
    logout(request)
    return redirect("main")


@login_required(login_url='login')
def change_password(request):
    form = PasswordChangeForm()
    user = request.user

    if request.method == 'POST':
        # если пользователь нажал "отмена", то возвращаем в личный кабинет
        if "cancel" in request.POST:
            return redirect("client_profile")
        else:
            # считываем форму, меняем пароль и авторизовываем обновленного пользователя
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                if check_password(form.cleaned_data['old_password'], user.password):
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    login(request, user)
                    return redirect("client_profile")
                else:
                    messages.error(request, "Неверный старый пароль")
            else:
                messages.error(request, "Не получилось сменить пароль")

    context = {'form': form, 'title': "Смена пароля"}
    return render(request, 'base/user_change.html', context=context)


@login_required(login_url='login')
def change_role(request):
    user = request.user

    # флаг, чтобы понять, добавлять объект client или удалять
    add_client = user.business_only

    if request.method == 'POST':
        # если пользователь нажал "отмена", то возвращаем в личный кабинет
        if "cancel" in request.POST:
            return redirect("client_profile")
        else:
            # добавляем/удаляем клиентский функционал
            if add_client:
                client = Client(user=user)
                client.save()
            else:
                client = user.client
                client.delete()

            user.business_only = not user.business_only
            user.save()
            return redirect("client_profile")

    # выбираем заголовок страницы в зависимости от типа пользователя
    if add_client:
        title = '''Вы уверены, что хотите добавить функционал клиента?
        Вы сможете искать исполнителей и записываться на услуги.'''
    else:
        title = '''Вы уверены, что хотите удалить функционал клиента и оставить только функционал для работы?
        Все ваши записи и подписки на организации безвозвратно удалятся.'''

    context = {'form': None, 'title': title}
    return render(request, 'base/user_change.html', context=context)


@login_required(login_url='login')
def change_user_info(request):

    user = request.user

    form = UserChangeForm(None, instance=user)

    if request.method == "POST":
        # если пользователь нажал "отмена", то возвращаем в личный кабинет
        if "cancel" in request.POST:
            return redirect("client_profile")
        else:
            form = UserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect("client_profile")
            else:
                messages.error(request, 'Не удалось изменить данные')

    context = {'form': form, 'title': "Редактировать профиль"}
    return render(request, 'base/user_change.html', context=context)