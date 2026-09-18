from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from companies.models import Company

from .forms import JobForm
from .models import Job


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
	raise_exception = True

	def test_func(self):
		return getattr(getattr(self.request.user, 'profile', None), 'role', None) == 'employer'


class JobListView(ListView):
	model = Job
	template_name = 'jobs/list.html'
	context_object_name = 'jobs'

	def get_queryset(self):
		query = self.request.GET.get('q', '').strip()
		jobs = Job.objects.filter(is_active=True).select_related('employer', 'company')
		if query:
			jobs = jobs.filter(
				Q(title__icontains=query)
				| Q(description__icontains=query)
				| Q(location__icontains=query)
			)
		return jobs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.request.GET.get('q', '').strip()
		return context


class JobDetailView(DetailView):
	model = Job
	template_name = 'jobs/detail.html'
	context_object_name = 'job'

	def get_queryset(self):
		return Job.objects.filter(is_active=True).select_related('employer', 'company')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['already_applied'] = (
			self.request.user.is_authenticated
			and self.object.applications.filter(applicant=self.request.user).exists()
		)
		return context


class JobCreateView(SuccessMessageMixin, EmployerRequiredMixin, CreateView):
	model = Job
	form_class = JobForm
	template_name = 'jobs/form.html'
	success_message = 'Job posted.'

	def form_valid(self, form):
		form.instance.employer = self.request.user
		company_name = form.cleaned_data.get('company_name')
		company = getattr(self.request.user, 'company', None)
		if company_name:
			if company is None:
				company = Company.objects.create(recruiter=self.request.user, name=company_name)
			else:
				company.name = company_name
				company.save(update_fields=['name'])
		form.instance.company = company
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('job_detail', kwargs={'pk': self.object.pk})


class EmployerJobMixin(EmployerRequiredMixin):
	def get_queryset(self):
		return Job.objects.filter(employer=self.request.user).select_related('company')


class ManageJobsView(EmployerJobMixin, ListView):
	model = Job
	template_name = 'jobs/manage.html'
	context_object_name = 'jobs'


class JobUpdateView(SuccessMessageMixin, EmployerJobMixin, UpdateView):
	model = Job
	form_class = JobForm
	template_name = 'jobs/form.html'
	success_url = reverse_lazy('manage_jobs')
	success_message = 'Job updated.'


class JobDeleteView(SuccessMessageMixin, EmployerJobMixin, DeleteView):
	model = Job
	template_name = 'jobs/confirm_delete.html'
	success_url = reverse_lazy('manage_jobs')
	success_message = 'Job deleted.'
