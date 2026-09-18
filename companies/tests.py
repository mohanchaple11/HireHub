from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Profile

from .models import Company


class CompanyFlowTests(TestCase):
	def setUp(self):
		self.recruiter = User.objects.create_user('recruiter', password='StrongPass123!')
		Profile.objects.create(user=self.recruiter, role=Profile.EMPLOYER)
		self.client.force_login(self.recruiter)

	def test_recruiter_can_create_company(self):
		response = self.client.post('/companies/manage/', {
			'name': 'Acme Labs', 'description': 'We build useful tools.',
			'website': 'https://example.com', 'location': 'Remote',
		})
		self.assertRedirects(response, '/companies/manage/')
		self.assertEqual(Company.objects.get(recruiter=self.recruiter).name, 'Acme Labs')

	def test_candidate_cannot_manage_company(self):
		candidate = User.objects.create_user('candidate', password='StrongPass123!')
		Profile.objects.create(user=candidate, role=Profile.CANDIDATE)
		self.client.force_login(candidate)
		self.assertEqual(self.client.get('/companies/manage/').status_code, 403)
