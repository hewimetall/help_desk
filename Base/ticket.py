from django.core.exceptions import FieldError
from django.db import models

class AbstractTicketBD(models.Model):

    STATUS = [
        (0, "В обработке"),
        (1, "Отправленно на доработку"),
        (2, "В работе"),
        (3, "Выполнена"),
        (4, "Закрыта"),
    ]

    title = models.CharField(max_length=50, verbose_name="Названия заявки")  # Названия заявки
    content = models.TextField(verbose_name="Текст обращения")  # Текст обращения

    status = models.IntegerField(choices=STATUS, default=STATUS[0][0], verbose_name="Статус заявки")  # Статус заявки
    
    # File = models.FileField(blank=True, null=True, default=None, upload_to="uploadFile/",
                            # verbose_name="Фаел")  # file Name

    data_created = models.DateField(auto_created=True, auto_now_add=True, db_index=True,
                                    verbose_name="Дата на момент создания")  # Дата на момент создания
    data_modifite = models.DateField(auto_created=True, auto_now=True, db_index=True,
                                     verbose_name="Дата последнего изменения")  # Дата на момент создания

    is_active = models.BooleanField(verbose_name = "Закрыта",default = True)

    def searchTuple(self, tups, elem):
        return [a for i, a in (filter(lambda tup: elem in tup, tups))]

    def getStatus(self):
        return self.searchTuple(self.STATUS, self.status)[0]

    def __str__(self):
        return f"{self.pk}:{self.title}"
    
    class Meta:
        abstract = True
