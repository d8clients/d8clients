from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def client_profile(request):
    user = request.user

    # выводим разные страницы для рабочих и клиентских аккаунтов
    if not user.is_client:
        context = {'user': user}
        return render(request, 'client/work_account_profile.html', context)

    context = {
        'user': user,
        'client': user.client,
        'subscribes': user.client.subscribes.all()
    }

    return render(request, 'client/client_profile.html', context)
