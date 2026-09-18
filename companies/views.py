from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from users.models import Profile

from .forms import CompanyForm
from .models import Company


def company_list(request):
	companies = Company.objects.all()
	return render(request, 'companies/list.html', {'companies': companies})


@login_required
def manage_company(request):
	if not hasattr(request.user, 'profile') or request.user.profile.role != Profile.EMPLOYER:
		raise PermissionDenied('Only recruiters can manage a company.')
	company, _ = Company.objects.get_or_create(recruiter=request.user, defaults={'name': f'{request.user.username} company'})
	form = CompanyForm(request.POST or None, instance=company)
	if form.is_valid():
		form.save()
		return redirect('company_manage')
	return render(request, 'companies/form.html', {'form': form, 'company': company})