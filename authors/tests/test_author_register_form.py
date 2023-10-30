from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Your first name'),
        ('last_name', 'Your last name'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('email', (
            'The e-mail must be valid.')),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lower case letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)