from django.db import models


class Application(models.Model):
	STATUS_CHOICES = [
		('application_sent', 'Application Sent'),
		('application_pending', 'Application Pending'),
		('shortlisted', 'Shortlisted'),
		('submitted', 'Submitted'),
		('reviewing', 'Reviewing'),
		('accepted', 'Accepted'),
		('rejected', 'Rejected'),
	]
	EXPERIENCE_CHOICES = [('fresher', 'Fresher'), ('experienced', 'Experienced')]

	job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
	applicant = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='applications')
	applicant_name = models.CharField(max_length=160, blank=True)
	applicant_email = models.EmailField(blank=True)
	applicant_phone = models.CharField(max_length=30, blank=True)
	education = models.CharField(max_length=200, blank=True)
	resume = models.FileField(upload_to='resumes/applications/', blank=True, null=True)
	experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True)
	experience_details = models.TextField(blank=True)
	cover_letter = models.TextField(blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [models.UniqueConstraint(fields=['job', 'applicant'], name='unique_job_applicant')]
