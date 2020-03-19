from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse

class LowerUsernameField(UsernameField):
    def to_python(self,date):
        return super().to_python(date.lower())

class LoginForm(AuthenticationForm):
    username = LowerUsernameField(widget=forms.TextInput(attrs={'autofocus': True,}), label="Логин")

    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput,
        )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))


class Login(LoginView):
    template_name = "login/autch/login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    # metods  return  url redirection
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        elif self.request.user.is_superuser:
            return reverse("admin:index")
        else:
            return reverse("dashBourdPage")

class Logout(LogoutView):
    template_name = "login/autch/logout.html"
