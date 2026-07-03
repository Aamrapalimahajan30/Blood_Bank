from django import forms
from donors.validators import validate_phone, validate_email, validate_blood_group
from donors.exceptions import InvalidPhoneError, InvalidEmailError, InvalidBloodGroupError

BLOOD_GROUP_CHOICES = [(g, g) for g in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']]
URGENCY_CHOICES = [('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('critical', 'Critical')]


class DonorRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    location = forms.CharField(max_length=100)

    def clean_phone(self):
        try:
            return validate_phone(self.cleaned_data['phone'])
        except InvalidPhoneError as e:
            raise forms.ValidationError(str(e))

    def clean_email(self):
        try:
            return validate_email(self.cleaned_data['email'])
        except InvalidEmailError as e:
            raise forms.ValidationError(str(e))

    def clean_blood_group(self):
        try:
            return validate_blood_group(self.cleaned_data['blood_group'])
        except InvalidBloodGroupError as e:
            raise forms.ValidationError(str(e))


class CampForm(forms.Form):
    name = forms.CharField(max_length=150)
    venue = forms.CharField(max_length=200)
    organizer = forms.CharField(max_length=150)
    camp_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField(max_length=100)


class BloodRequestForm(forms.Form):
    hospital = forms.CharField(max_length=150)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES)
    location = forms.CharField(max_length=100)
    units_needed = forms.IntegerField(min_value=1, initial=1)
    urgency = forms.ChoiceField(choices=URGENCY_CHOICES, initial='normal')

    def clean_blood_group(self):
        try:
            return validate_blood_group(self.cleaned_data['blood_group'])
        except InvalidBloodGroupError as e:
            raise forms.ValidationError(str(e))


class CampRegistrationForm(forms.Form):
    camp_id = forms.CharField(max_length=50)
    donor_id = forms.CharField(max_length=50)