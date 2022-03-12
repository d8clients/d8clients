from django.shortcuts import render, redirect
from .forms import CreateOrg
from .models import Organization
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def organizations_main_page(request):
    context = {}
    return render(request, 'organization/organizations_main_page.html', context)


@login_required(login_url='login')
def create_organization(request):

    form = CreateOrg()

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect("client_profile")
        else:
            form = CreateOrg(request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                Organization.objects.create(
                    name=cd['name'],
                    description=cd['description'],
                    owner=request.user
                )
                return redirect("org_main")
            else:
                messages.error(request, "Не получилось создать организацию")

    context = {'form': form}
    return render(request, 'organization/create_organization.html', context=context)


