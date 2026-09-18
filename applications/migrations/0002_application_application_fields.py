from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='applicant_name',
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name='application',
            name='education',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='application',
            name='experience_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='application',
            name='experience_level',
            field=models.CharField(blank=True, choices=[('fresher', 'Fresher'), ('experienced', 'Experienced')], max_length=20),
        ),
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/applications/'),
        ),
    ]