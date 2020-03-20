from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit
from django import forms

class CrispyModelFormMixim():
    def __init__(self, *args, **kwargs):
        super(CrispyModelFormMixim, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = "form_app"
        self.setting()

    def setting(self):
        self.helper.add_input(Submit('отправить', 'Отправить'))
