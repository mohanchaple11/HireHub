from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Profile

from .models import Job


class JobFlowTests(TestCase):
	def setUp(self):
		self.employer = User.objects.create_user('employer', password='StrongPass123!')
		Profile.objects.create(user=self.employer, role=Profile.EMPLOYER)
		Job.objects.create(employer=self.employer, title='Django Developer', description='Build APIs', location='Remote')

	def test_search_finds_matching_jobs(self):
		response = self.client.get('/jobs/?q=django')
		self.assertContains(response, 'Django Developer')

	def test_candidate_cannot_post_a_job(self):
		candidate = User.objects.create_user('candidate', password='StrongPass123!')
		Profile.objects.create(user=candidate, role=Profile.CANDIDATE)
		self.client.force_login(candidate)
		response = self.client.get('/jobs/new/')
		self.assertEqual(response.status_code, 403)

	def test_recruiter_can_manage_and_edit_owned_job(self):
		self.client.force_login(self.employer)
		job = Job.objects.filter(employer=self.employer).first()
		response = self.client.post(f'/jobs/{job.pk}/edit/', {
			'title': 'Senior Django Developer', 'description': 'Build APIs', 'location': 'Remote',
			'employment_type': 'full-time', 'salary': '', 'is_active': 'on',
		})
		self.assertRedirects(response, '/jobs/manage/')
		self.assertEqual(Job.objects.get(pk=job.pk).title, 'Senior Django Developer')

	def test_recruiter_can_create_a_job(self):
		self.client.force_login(self.employer)
		response = self.client.post('/jobs/new/', {
			'title': 'Python Engineer', 'description': 'Build services', 'location': 'Remote',
			'employment_type': 'full-time', 'salary': '', 'is_active': 'on',
		})
		job = Job.objects.get(title='Python Engineer')
		self.assertRedirects(response, f'/jobs/{job.pk}/')
		self.assertEqual(job.employer, self.employer)

	def test_active_job_detail_is_public(self):
		job = Job.objects.filter(employer=self.employer).first()
		response = self.client.get(f'/jobs/{job.pk}/')
		self.assertContains(response, 'Django Developer')

	def test_recruiter_can_delete_owned_job(self):
		self.client.force_login(self.employer)
		job = Job.objects.filter(employer=self.employer).first()
		response = self.client.post(f'/jobs/{job.pk}/delete/')
		self.assertRedirects(response, '/jobs/manage/')
		self.assertFalse(Job.objects.filter(pk=job.pk).exists())

	def test_recruiter_cannot_delete_another_recruiters_job(self):
		other = User.objects.create_user('other', password='StrongPass123!')
		Profile.objects.create(user=other, role=Profile.EMPLOYER)
		job = Job.objects.filter(employer=self.employer).first()
		self.client.force_login(other)
		response = self.client.post(f'/jobs/{job.pk}/delete/')
		self.assertEqual(response.status_code, 404)
		self.assertTrue(Job.objects.filter(pk=job.pk).exists())
