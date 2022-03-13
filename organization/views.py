from django.shortcuts import render, redirect
from .forms import CreateOrg
from .models import Organization
from staff.models import Admin
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    print(user.is_admin)
    print(user.is_employee)
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
    org = Organization.objects.get(id=pk)

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
    if request.user.admin.filter(organization=org).count():
        print(request.user.admin.filter(organization=org))
        is_admin = True
    if request.user.employee.filter(organization=org).count():
        print(request.user.employee.filter(organization=org))
        is_staff = True

    context = {'user': request.user,
               'org': org, 'subscribed': subscribed,
               'is_admin': is_admin, 'is_staff': is_staff}
    return render(request, 'organization/organization_profile.html', context=context)


@login_required(login_url='login')
def organization_edit_mode(request, pk):

    org = Organization.objects.get(id=pk)
    if org.admins.filter(user=request.user).first is None:
        return redirect('org_profile', pk)

    context = {'user': request.user,
               'org': org}
    return render(request, 'organization/organization_edit_mode.html', context=context)