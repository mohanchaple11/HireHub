from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
	recruiter = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
	name = models.CharField(max_length=160)
	description = models.TextField(blank=True)
	website = models.URLField(blank=True)
	location = models.CharField(max_length=120, blank=True)

	def __str__(self):
		return self.name
