from django.test import TestCase
from django.test import Client
from .form_ticket import FormTicketBD
from Base.models import CustomUser
from Base.models import CustomGroup


class Setup_Class(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="user@mp.com", password="user", first_name="user", phone=12345678)

class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = FormTicketBD("manager").form
        form = form(data={'groups':CustomGroup.objects.all()[0].name, 'maneger':CustomUser.objects.all()[0],'status':False})
        assert form.is_valid() ,"manager"
        
        form = FormTicketBD("autor").form
        form = form(data={'groups':CustomGroup.objects.all()[0].name, 'title':"test", 'content':"BODY ff"})
        assert form.is_valid() ,"autor"
        
        form = FormTicketBD("anon").form
        assert form.is_valid() ,"anon"
        
        self.assertTrue(True)

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = FormTicketBD("autor").form
        form = form(data={'groups':CustomGroup.objects.all()[0].name, 'maneger':CustomUser.objects.all()[0],'status':False})

        self.assertFalse(form.is_valid())