from django import forms
from django.forms import ModelForm
from .models import Doctor, Speciality, DoctorSpeciality, Service, DoctorSpecialityService, Schedule, Appointment

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

class NewAppointmentForm(forms.Form):
    service = forms.ModelChoiceField(queryset=None)
    date = forms.ModelChoiceField(queryset=None)

    def __init__(self, doc_spec_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = DoctorSpeciality.objects.get(id__exact=doc_spec_id).doctorspecialityservice_set.all()
        self.fields["date"].queryset = DoctorSpeciality.objects.get(id__exact=doc_spec_id).doctor.schedule_set.all().filter(available__exact='a')

class AppointmentUserChangeForm(forms.Form):
    date = forms.ModelChoiceField(queryset=None)

    def __init__(self, doc_spec_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].queryset = DoctorSpeciality.objects.get(
            id__exact=doc_spec_id).doctor.schedule_set.all().filter(available__exact='a')

    # def clean_renewal_date(self):
    #     data = self.cleaned_data['renewal_date']
    #
    #     if not data:
    #         raise ValidationError('Invalid date - renewal in past')
    #
    #     if not data:
    #         raise ValidationError('Invalid date - renewal more than 4 weeks ahead')
    #
    #     return data
