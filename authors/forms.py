from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        # exclude = ['first_name'] # exclude item from form

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'Password': 'Password',
        }

        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'invalid': 'This field is invalid'
            },
            'password': {
                'required': 'This field must not be empty',
                'invalid': 'This field is invalid'
            }
        }

        widgets = {
            # each field have different widget
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here.',
                'class': 'input text-input outra-classe'
            }),
            'password': forms.PasswordInput(attrs={ # field has password type "***"
                'placeholder': 'Type your password here.'
            })
        }