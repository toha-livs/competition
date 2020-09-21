from django.db import models


class BaseNameModel(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class BaseDateTimeModel(models.Model):
    created_dt = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_dt = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True
