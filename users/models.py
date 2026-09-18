from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
	CANDIDATE = 'candidate'
	EMPLOYER = 'employer'
	ROLE_CHOICES = [(CANDIDATE, 'Job seeker'), (EMPLOYER, 'Recruiter')]

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)
	phone = models.CharField(max_length=30, blank=True)
	bio = models.TextField(blank=True)
	resume = models.FileField(upload_to='resumes/', blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} ({self.get_role_display()})'
