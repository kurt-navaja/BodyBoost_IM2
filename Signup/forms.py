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
    
class KnowMoreForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'weight', 'height', 'age', 'body_goal', 'gender', 'receive_emails', 'agree_to_terms')
        widgets = {
            'body_goal': forms.Select(choices=CustomUser.BODY_GOAL_CHOICES, attrs={'class': 'bacaltos-sign-up-page2-text22'}),
            'gender': forms.RadioSelect(choices=CustomUser.GENDER_CHOICES),
            'receive_emails': forms.CheckboxInput(attrs={'class': 'hidden-checkbox'}),
            'agree_to_terms': forms.CheckboxInput(attrs={'class': 'hidden-checkbox', 'required': True}),
        }
        
    def __init__(self, *args, **kwargs):
        super(KnowMoreForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text12',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text14',
            'placeholder': 'Last Name'
        })
        self.fields['weight'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text16',
            'placeholder': 'Weight',
            'min': '30',
            'max': '300',
            'step': '0.1'
        })
        self.fields['height'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text18',
            'placeholder': 'Height',
            'min': '100',
            'max': '250',
            'step': '0.1'
        })
        self.fields['age'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text20',
            'placeholder': 'Age',
            'min': '5',
            'max': '120'
        })
        self.fields['body_goal'].widget.attrs.update({
            'class': 'bacaltos-sign-up-page2-text22',
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'gender-option',
        })
        
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and (weight < 30 or weight > 300):
            raise forms.ValidationError("Weight must be between 30 and 300 kg.")
        return weight

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None and (height < 100 or height > 250):
            raise forms.ValidationError("Height must be between 100 and 250 cm.")
        return height

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 5 or age > 120):
            raise forms.ValidationError("Age must be between 5 and 120 years.")
        return age