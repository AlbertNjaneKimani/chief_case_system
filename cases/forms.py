from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, Case, Appointment

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'national_id', 'gender', 'location', 'sublocation', 'county']

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['title', 'description','casecategory']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput())    

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'location']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        if date and time:
            existing_appointment = Appointment.objects.filter(date=date, time=time, appointment_status='active').exists()
            if existing_appointment:
                self.add_error(None, forms.ValidationError("Appointment already booked for this date and time. Please select a different date or time."))
        return cleaned_data
  