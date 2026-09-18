from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile


class AccountFlowTests(TestCase):
	def test_register_login_and_update_profile_without_resume(self):
		response = self.client.post('/users/register/', {
			'username': 'candidate', 'email': 'candidate@example.com', 'role': 'candidate',
			'password1': 'StrongPass123!', 'password2': 'StrongPass123!',
		})
		self.assertRedirects(response, '/dashboard/')
		self.assertTrue(self.client.session.get('_auth_user_id'))

		response = self.client.post('/users/profile/', {
			'email': 'candidate@example.com', 'phone': '555-0100', 'bio': 'Python developer',
		})
		self.assertRedirects(response, '/users/profile/')
		self.assertEqual(Profile.objects.get(user__username='candidate').phone, '555-0100')
		self.assertFalse(Profile.objects.get(user__username='candidate').resume)

	def test_role_is_persisted_on_registration(self):
		self.client.post('/users/register/', {
			'username': 'employer', 'email': 'employer@example.com', 'role': 'employer',
			'password1': 'StrongPass123!', 'password2': 'StrongPass123!',
		})
		self.assertEqual(User.objects.get(username='employer').profile.role, Profile.EMPLOYER)

	def test_employer_can_browse_and_search_candidate_profiles(self):
		employer = User.objects.create_user('employer2', password='StrongPass123!')
		Profile.objects.create(user=employer, role=Profile.EMPLOYER)
		candidate = User.objects.create_user('designer', first_name='Maya', password='StrongPass123!')
		Profile.objects.create(user=candidate, role=Profile.CANDIDATE, bio='Product designer with research experience.')
		self.client.force_login(employer)

		response = self.client.get('/users/candidates/?q=research')
		self.assertContains(response, 'Maya')
		self.assertContains(response, 'Product designer')
		response = self.client.get(f'/users/candidates/{candidate.profile.pk}/')
		self.assertContains(response, 'Product designer with research experience.')

	def test_candidate_cannot_browse_other_candidate_profiles(self):
		candidate = User.objects.create_user('candidate2', password='StrongPass123!')
		Profile.objects.create(user=candidate, role=Profile.CANDIDATE)
		self.client.force_login(candidate)
		self.assertEqual(self.client.get('/users/candidates/').status_code, 403)
