from django.db import models


class Job(models.Model):
    EMPLOYMENT_CHOICES = [('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contract', 'Contract')]

    employer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posted_jobs')
    company = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    title = models.CharField(max_length=160)
    description = models.TextField()
    location = models.CharField(max_length=120)
    vacancies = models.PositiveIntegerField(default=1)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='full-time')
    salary = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
