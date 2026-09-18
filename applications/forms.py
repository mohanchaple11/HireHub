from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    applicant_name = forms.CharField(label='Full name', max_length=160)
    applicant_email = forms.EmailField(label='Email ID')
    applicant_phone = forms.CharField(label='Phone number', max_length=30)
    education = forms.CharField(label='Education', max_length=200)
    experience_level = forms.ChoiceField(label='Experience', choices=Application.EXPERIENCE_CHOICES)
    experience_details = forms.CharField(
        label='Experience details',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='For experienced applicants, describe your relevant experience. Fresher applicants can leave this blank.',
    )
    class Meta:
        model = Application
        fields = ('applicant_name', 'applicant_email', 'applicant_phone', 'education', 'resume', 'experience_level', 'experience_details', 'cover_letter')
        labels = {'cover_letter': 'Cover letter'}
        widgets = {'cover_letter': forms.Textarea(attrs={'rows': 8})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None and not self.is_bound:
            self.fields['applicant_name'].initial = user.get_full_name() or user.username
            self.fields['applicant_email'].initial = user.email
            self.fields['applicant_phone'].initial = getattr(user.profile, 'phone', '')
