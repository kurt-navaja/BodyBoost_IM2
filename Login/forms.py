from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'bacaltos-sign-up-page-text14',
            'placeholder': 'Email Address'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        
        return email

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bacaltos-sign-up-page-text16',
            'placeholder': 'New Password'
        }),
        label="New Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bacaltos-sign-up-page-text18',
            'placeholder': 'Confirm New Password'
        }),
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match. Please try again.")
            
            try:
                # Validate password strength using Django's validators
                validate_password(password1)
            except forms.ValidationError as e:
                self.add_error('password1', e)

        return cleaned_data