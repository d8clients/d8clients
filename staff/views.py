from django.shortcuts import render, redirect
from .models import Employee, WorkDay
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from organization.views import edit_org_perm
from .forms import EditEmployee, WorkDayForm
from organization.forms import AddEmployee


def employee_profile(request, pk):
    """
        профиль сотрудника
    """
    # проверяем, существует ли такой сотрудник
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    context = {'employee': employee,
               'is_admin': edit_org_perm(request.user, employee.organization),
               'services': employee.services.all()
               }

    return render(request, "staff/employee_profile.html", context=context)


def edit_employee(request, pk):
    """
        администратор редактирует
        данные о сотруднике
    """
    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    org = employee.organization
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', org.id)

    form = EditEmployee(None,
                        organization=org,
                        instance=employee,
                        initial={
                            "services": [service for service in employee.services.all().values_list("id", flat=True)]
                        })

    if request.method == "POST":
        # если пользователь нажал "отмена", то возвращаем в личный кабинет
        if "cancel" in request.POST:
            return redirect("employee_profile", employee.id)
        else:
            form = EditEmployee(request.POST, organization=org, instance=employee)
            if form.is_valid():
                form.save()
                return redirect("employee_profile", employee.id)
            else:
                messages.error(request, 'Не удалось изменить данные')

    context = {'form': form, 'title': "Редактировать информацию о сотруднике"}
    return render(request, 'staff/edit_staff.html', context=context)


@login_required(login_url='login')
def edit_timetable(request, pk):
    """
        администратор редактирует
        расписание сотрудника
    """

    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    org = employee.organization
    if not edit_org_perm(request.user, org):
        return redirect('org_profile', org.id)

    form = WorkDayForm()

    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('employee_profile', pk)
        else:
            form = WorkDayForm(request.POST)
            if form.is_valid():
                WorkDay.objects.filter(employee=employee).filter(date=form.cleaned_data['date']).delete()
                workday = form.save(commit=False)
                workday.employee = employee
                workday.save()
                messages.success(request, "Расписание изменено!")

    context = {'form': form, 'title': "Редактировать расписание"}
    return render(request, 'staff/edit_timetable.html', context=context)


@login_required(login_url='login')
def employee_assignments(request, pk):

    try:
        employee = Employee.objects.get(id=pk)
    except Employee.DoesNotExist:
        messages.error(request, "Такого сотрудника не существует")
        return redirect('org_main')

    if not request.user.employee.filter(id=pk).exists():
        return redirect("employee_profile", pk)

    context = {'employee': employee,
               'assignments': employee.assignments.all().order_by('date')}
    return render(request, 'staff/employee_assignments.html', context=context)
