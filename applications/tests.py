from django.test import TestCase
from django.contrib.auth.models import User

from jobs.models import Job
from users.models import Profile

from .models import Application


class ApplicationFlowTests(TestCase):
	def setUp(self):
		employer = User.objects.create_user('employer', password='StrongPass123!')
		Profile.objects.create(user=employer, role=Profile.EMPLOYER)
		self.job = Job.objects.create(employer=employer, title='Designer', description='Design products', location='Remote')
		self.candidate = User.objects.create_user('candidate', password='StrongPass123!')
		Profile.objects.create(user=self.candidate, role=Profile.CANDIDATE)
		self.client.force_login(self.candidate)

	def test_candidate_can_apply_and_track_status(self):
		response = self.client.post(f'/applications/apply/{self.job.pk}/', {
			'applicant_name': 'Candidate User',
			'applicant_email': 'candidate@example.com',
			'applicant_phone': '+91 9876543210',
			'education': 'BSc Computer Science',
			'experience_level': 'fresher',
			'experience_details': '',
			'cover_letter': 'I would love to help.',
		})
		self.assertRedirects(response, '/applications/')
		application = Application.objects.get(job=self.job, applicant=self.candidate)
		self.assertEqual(application.status, 'submitted')
		self.assertEqual(application.applicant_email, 'candidate@example.com')
		self.assertEqual(application.applicant_phone, '+91 9876543210')
		response = self.client.get('/applications/')
		self.assertContains(response, 'Submitted')

	def test_candidate_cannot_apply_twice(self):
		Application.objects.create(job=self.job, applicant=self.candidate)
		response = self.client.post(f'/applications/apply/{self.job.pk}/', {'cover_letter': 'Again'})
		self.assertRedirects(response, f'/jobs/{self.job.pk}/')
		self.assertEqual(Application.objects.filter(job=self.job, applicant=self.candidate).count(), 1)

	def test_recruiter_can_update_application_status(self):
		application = Application.objects.create(job=self.job, applicant=self.candidate)
		recruiter = self.job.employer
		self.client.force_login(recruiter)
		response = self.client.post(f'/applications/{application.pk}/status/', {'status': 'reviewing'})
		self.assertRedirects(response, '/applications/received/')
		self.assertEqual(Application.objects.get(pk=application.pk).status, 'reviewing')
		response = self.client.get('/applications/received/')
		self.assertContains(response, 'reviewing')
