from django.shortcuts import render, redirect
from .forms import CreateOrg, AddAdmin, AddEmployee
from .models import Organization
from staff.models import Admin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import User
from staff.models import Admin, Employee


def organizations_main_page(request):
    """
        переводит разные типы пользователей на более
        актуальные для их ролей страницы
    """
    if request.user.is_anonymous:
        return redirect('search_org')
    if request.user.is_client:
        return redirect('org_sub')
    return redirect('work_org')


@login_required(login_url='login')
def organization_subscribes(request):
    """
        выводит список подписок пользователя-клиента,
        иначе переводит его на главную
    """

    user = request.user
    if not user.is_client:
        return redirect("org_main")

    context = {'user': user,
               'subscribes': user.client.subscribes.all()}
    return render(request, 'organization/organizations_my_subscribes.html', context=context)


@login_required(login_url='login')
def organization_work(request):
    """
            выводит список организаций, в которых
            работает пользователь
    """

    user = request.user
    if not user.is_staff:
        return redirect("org_main")

    context = {
        'user': user,
        'admin_work': [admin.organization for admin in user.admin.all()],
        'employee_work': [employee.organization for employee in user.employee.all()]
    }
    return render(request, 'organization/work_list_org.html', context=context)


@login_required(login_url='login')
def create_organization(request):
    """
        создание новой организации для
        авторизованный пользователей
    """
    form = CreateOrg()

    if request.method == 'POST':
        # если пользователь нажал на "отмена", то возвращаем его на страницу с организациями
        if "cancel" in request.POST:
            return redirect("org_main")
        else:
            form = CreateOrg(request.POST)
            # если форма корректна, создаем новую организацию и делаем пользователя её администратором
            if form.is_valid():
                cd = form.cleaned_data
                org = Organization.objects.create(
                    name=cd['name'],
                    description=cd['description'],
                    owner=request.user,
                    name_low=cd['name'].lower()
                )
                Admin.objects.create(
                    user=request.user,
                    organization=org,
                    is_host=True
                )

                if request.user.is_client:
                    request.user.client.subscribes.add(org)

                # перенаправляем на профиль организации
                return redirect("org_profile", pk=org.id)

            else:
                messages.error(request, "Не получилось создать организацию")

    context = {'form': form, 'user': request.user}
    return render(request, 'organization/create_organization.html', context=context)


def search_organization(request):
    """
           поиск организаций по имени для
           пользователей с функционалом клиента
    """
    # проверям, что аккаунт не только для работы
    user = request.user
    if user.is_authenticated and not user.is_client:
        return redirect("org_main")

    # получаем запрос от пользователя
    q = request.GET.get('q')
    # если запроса не было, или если это пустая строка, то ничего не ищем
    if q is not (None or ''):
        organizations = Organization.objects.filter(name_low__icontains=str(q).lower())
    else:
        organizations = []

    context = {'user': user, 'organizations': organizations}
    return render(request, 'organization/search_organization.html', context=context)


def organization_profile(request, pk):

    try:
        org = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        messages.error(request, "Такой организации не существует")
        return redirect('org_main')

    # подписываем/отписываем клиента в зависимости от формы
    if request.method == "POST":
        client = request.user.client
        if 'Подписаться' in request.POST:
            client.subscribes.add(org)
        if 'Отписаться' in request.POST:
            client.subscribes.remove(org)

    # смотрим, подписан ли пользователь на эту организацию
    subscribed = 'Подписаться'
    if request.user.is_authenticated and request.user.is_client:
        client = request.user.client
        if org in client.subscribes.all():
            subscribed = 'Отписаться'

    # проверяем, относится ли пользователь к персоналу организации
    is_admin = False
    is_staff = False
    if request.user.is_authenticated:
        if request.user.admin.filter(organization=org).count():
            print(request.user.admin.filter(organization=org))
            is_admin = True
        if request.user.employee.filter(organization=org).count():
            print(request.user.employee.filter(organization=org))
            is_staff = True

    employees = org.employees.filter(confirmed=True)

    context = {
        'user': request.user,
        'org': org, 'subscribed': subscribed,
        'is_admin': is_admin, 'is_staff': is_staff,
        'employees': employees
    }

    return render(request, 'organization/organization_profile.html', context=context)


def edit_org_perm(user, org):
    # проверяем, является ли пользователь администратором организации
    return org.admins.filter(user=user).exists()


@login_required(login_url='login')
def organization_edit_mode(request, pk):

    try:
        org = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        messages.error(request, "Такой организации не существует")
        return redirect('org_main')

    if not edit_org_perm(request.user, org):
        return redirect('org_profile', pk)

    conf_employees = org.employees.filter(confirmed=True)
    unconf_employees = org.employees.filter(confirmed=False)

    conf_admins = org.admins.filter(confirmed=True)
    unconf_admins = org.admins.filter(confirmed=False)

    context = {
        'user': request.user,
        'org': org,
        'conf_employees': conf_employees,
        'unconf_employees': unconf_employees,
        'conf_admins': conf_admins,
        'unconf_admins': unconf_admins,
    }
    return render(request, 'organization/organization_edit_mode.html', context=context)


@login_required(login_url='login')
def add_employee(request, pk):
    """
        администратор добавляет
        нового сотрудника в организацию
    """
    # проверяем, есть ли такая организация
    try:
        org = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        messages.error(request, "Такой организации не существует")
        return redirect('org_main')

    # проверяем, что у пользователя достаточно прав
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', pk)

    form = AddEmployee()

    if request.method == 'POST':
        # если пользователь нажал "отмена", то возвращаем его
        if "cancel" in request.POST:
            return redirect('org_edit', pk)
        else:
            form = AddEmployee(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']

                # проверяем, существует ли человек с таким e-mail
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    # проверяем, есть ли уже такой сотрудник
                    if not user.employee.filter(organization=org).exists():
                        employee = Employee.objects.create(
                            user=user,
                            organization=org,
                            bio="",
                            confirmed=False
                        )
                        return redirect('org_edit', pk=org.id)
                    else:
                        messages.error(request, "Вы уже добавили этого пользователя в сотрудники")
                else:
                    messages.error(request, "Пользователя с таким e-mail не существует")
            else:
                messages.error(request, "Не получилось добавить сотрудника")

    context = {
        'user': request.user,
        'org':  org,
        'form': form,
        'title': 'Добавить сотрудника'
    }
    return render(request, 'organization/edit_org_forms.html', context=context)


@login_required(login_url='login')
def add_admin(request, pk):
    """
        администратор добавляет
        нового администратора в организацию
    """
    # проверяем, есть ли такая организация
    try:
        org = Organization.objects.get(id=pk)
    except Organization.DoesNotExist:
        messages.error(request, "Такой организации не существует")
        return redirect('org_main')

    # проверяем, что у пользователя достаточно прав
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', pk)

    form = AddEmployee()

    if request.method == 'POST':
        # если пользователь нажал "отмена", то возвращаем его
        if "cancel" in request.POST:
            return redirect('org_edit', pk)
        else:
            form = AddAdmin(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']

                # проверяем, существует ли человек с таким e-mail
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    # проверяем, есть ли уже такой сотрудник
                    if not user.admin.filter(organization=org).exists():
                        admin = Admin.objects.create(
                            user=user,
                            organization=org,
                            confirmed=False
                        )
                        return redirect('org_edit', pk=org.id)
                    else:
                        messages.error(request, "Вы уже добавили этого пользователя в администраторы")
                else:
                    messages.error(request, "Пользователя с таким e-mail не существует")
            else:
                messages.error(request, "Не получилось добавить администратора")

    context = {
        'user': request.user,
        'org':  org,
        'form': form,
        'title': 'Добавить администратора'
    }
    return render(request, 'organization/edit_org_forms.html', context=context)


@login_required(login_url='login')
def delete_employee(request, pk):
    """
            администратор удаляет сотрудника
            из организации
    """
    # проверяем, есть ли такой сотрудник
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    org = employee.organization

    # проверяем, что у пользователя достаточно прав
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', org.id)

    employee.delete()

    return redirect('org_edit', org.id)


@login_required(login_url='login')
def delete_admin(request, pk):
    """
            администратор удаляет администратора
            из организации
    """

    # проверяем, есть ли такой администратор
    try:
        admin = Admin.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    org = admin.organization

    # проверяем, что у пользователя достаточно прав
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', org.id)

    if admin.user == request.user:
        messages.error(request, 'Вы не можете сами удалить себя из организации')
        return redirect('org_edit', org.id)

    if not admin.is_host:
        admin.delete()
    else:
        messages.error(request, 'Вы не удалить владельца организации')

    return redirect('org_edit', org.id)
