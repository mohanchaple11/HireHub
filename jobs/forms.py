from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    vacancies = forms.IntegerField(min_value=1, required=False, initial=1, label='Number of vacancies')
    company_name = forms.ChoiceField(
        choices=[
            ('', 'Select a company'),
            ('Softech solution', 'Softech solution'),
            ('Softtrust', 'Softtrust'),
            ('Zappcode solution', 'Zappcode solution'),
            ('ZS solution', 'ZS solution'),
            ('PSK Technology', 'PSK Technology'),
        ],
        required=False,
        label='Company name',
    )

    class Meta:
        model = Job
        fields = ('title', 'description', 'location', 'vacancies', 'employment_type', 'salary', 'is_active')
        widgets = {'description': forms.Textarea(attrs={'rows': 6})}

    def clean_vacancies(self):
        return self.cleaned_data.get('vacancies') or 1
