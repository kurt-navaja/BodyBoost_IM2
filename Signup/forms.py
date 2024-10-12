from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['email', 'phone_number', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['email'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page-text14',
            'placeholder': 'Email'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page-text20',
            'placeholder': 'Phone Number'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page-text16',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page-text18',
            'placeholder': 'Confirm Password'
        })
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Please enter only numeric characters for the phone number.")
        return phone_number