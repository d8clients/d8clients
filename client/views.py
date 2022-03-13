from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def client_profile(request):
    user = request.user

    employee_req = user.employee.filter(confirmed=False)
    admin_req = user.admin.filter(confirmed=False)

    # если полльзователь ответил на какую-то заявку о работе
    if request.method == 'POST':
        for employee in employee_req:
            # если подтвердил работу сотрудника
            if f'accept_employee_{employee.organization.id}' in request.POST:
                employee.confirmed = True
                employee.save()
                # добавляем организацию в подписки
                if user.is_client:
                    user.client.subscribes.add(employee.organization)

            # если отклонил работу сотрудника
            if f'reject_employee_{employee.organization.id}' in request.POST:
                employee.delete()

        for admin in admin_req:
            # если подтвердил работу администратора
            if f'accept_admin_{admin.organization.id}' in request.POST:
                admin.confirmed = True
                admin.save()
                # добавляем организацию в подписки
                if user.is_client:
                    user.client.subscribes.add(admin.organization)

            # если отклонил работу администратора
            if f'reject_admin_{admin.organization.id}' in request.POST:
                admin.delete()

        employee_req = user.employee.filter(confirmed=False)
        admin_req = user.admin.filter(confirmed=False)

    # выводим разные страницы для рабочих и клиентских аккаунтов
    if not user.is_client:

        context = {
            'user': user,

            'employee_req': employee_req,
            'employee_req_exist': employee_req.exists(),
            'admin_req': admin_req,
            'admin_req_exist': admin_req.exists(),

            'admin_work': [admin.organization for admin in user.admin.all()],
            'employee_work': [employee.organization for employee in user.employee.all()]

        }
        return render(request, 'client/work_account_profile.html', context)

    context = {
        'user': user,
        'client': user.client,
        'subscribes': user.client.subscribes.all(),
        'employee_req': employee_req,
        'employee_req_exist': employee_req.exists(),
        'admin_req': admin_req,
        'admin_req_exist': admin_req.exists()
    }

    return render(request, 'client/client_profile.html', context)
