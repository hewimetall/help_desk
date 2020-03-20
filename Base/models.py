from django.db import models
from django.contrib.auth.models import AbstractUser,Group

from django.utils.translation import gettext_lazy as _
from .ticket import AbstractTicketBD
from .ticker_meneger import TicketBDManeger
from simple_history.models import HistoricalRecords

# Create your models here.
#Model user +
#      usename group fullname password   
#model group +
#      name username_id is_active
#model ticker +
#      title content status  is_active autor manager data_created data_modifite ,histori
#model chatTicker 
#      post name body data_created data_modifite

class CustomGroup(Group):
    is_visible = models.BooleanField(default=False)

class CustomUser(AbstractUser):
    
    groups = models.ManyToManyField(
        CustomGroup,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    full_name=models.CharField(max_length=100,verbose_name="ФИО")

TicketBDManeger.CustomModels=CustomUser

class TicketBD(AbstractTicketBD):
    objects = TicketBDManeger()

    autors = models.ForeignKey(CustomUser, related_name='autorsCr', on_delete=models.DO_NOTHING,
                               verbose_name="Автор обращения",null=True)  # Автор обращения
    maneger = models.ForeignKey(CustomUser, related_name='manager_aCr', on_delete=models.DO_NOTHING, blank=True,
                                null=True, verbose_name="Ответственный")  # Ответственный
    groups = models.ForeignKey(CustomGroup, related_name='groups_aCr', on_delete=models.DO_NOTHING,
                               verbose_name="Подразделения")  # Подразделения

    history = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

class TicketChat(models.Model):
    post = models.ForeignKey(TicketBD, related_name='chat', on_delete=models.CASCADE, db_column='pk', blank=False)
    name = models.ForeignKey(CustomUser, related_name='userCreated', on_delete=models.DO_NOTHING, db_column='username')
    body = models.TextField()
    file = models.FileField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'by {} on {}'.format(self.name, self.post)
