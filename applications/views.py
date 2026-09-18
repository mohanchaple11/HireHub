from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Job

from .forms import ApplicationForm
from .models import Application


@login_required
def apply(request, job_id):
	if not hasattr(request.user, 'profile') or request.user.profile.role != 'candidate':
		raise PermissionDenied('Only candidates can apply for jobs.')
	job = get_object_or_404(Job, pk=job_id, is_active=True)
	if Application.objects.filter(job=job, applicant=request.user).exists():
		messages.info(request, 'You have already applied for this job.')
		return redirect('job_detail', pk=job.pk)
	form = ApplicationForm(request.POST or None, request.FILES or None, user=request.user)
	if form.is_valid():
		application = form.save(commit=False)
		application.job = job
		application.applicant = request.user
		application.save()
		messages.success(request, 'Application submitted.')
		return redirect('my_applications')
	return render(request, 'applications/form.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
	applications = Application.objects.filter(applicant=request.user).select_related('job')
	return render(request, 'applications/list.html', {'applications': applications, 'employer_view': False})


@login_required
def employer_applications(request):
	if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
		raise PermissionDenied('Only employers can view received applications.')
	applications = Application.objects.filter(job__employer=request.user).select_related('job', 'applicant')
	return render(request, 'applications/list.html', {'applications': applications, 'employer_view': True})


@login_required
def update_status(request, application_id):
	if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
		raise PermissionDenied('Only recruiters can update application status.')
	application = get_object_or_404(Application, pk=application_id, job__employer=request.user)
	if request.method == 'POST' and request.POST.get('status') in dict(Application.STATUS_CHOICES):
		application.status = request.POST['status']
		application.save(update_fields=['status'])
		messages.success(request, 'Application status updated.')
	return redirect('employer_applications')


