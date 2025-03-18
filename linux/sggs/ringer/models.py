from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

import getpass

user = "/home/" + getpass.getuser()

class UploadFile(models.Model):
    type_ring = {
        "default": "Стандартный",
        "23feb": "23 февраля",
        "8mar": "8 марта",
        "1may": "1 мая",
        "9may": "9 мая",
        "1sep": "1 сентября",
        "halloween": "Хеллоуин",
        "4nov": "4 ноября",
        "ny": "Новый год",
    }
    title = models.CharField(max_length=50, verbose_name="Тип звонка", choices=type_ring, default=type_ring["default"])

    def __str__(self):
        return str(self.title)


class LessonQuantity(models.Model):
    """
    Подсчет уроков из программы
    """
    
    count_num = models.IntegerField()
    count_num = str(sum(1 for line in open(f'{user}/sggs/ringer/app/ringer.py', 'r') if "day.at(pre" in line))
    num = models.IntegerField(default=count_num, verbose_name="Сколько уроков будет?:")

    def __str__(self):
        """
        Строка для представления модели в удобочитаемом имени (in Admin site etc.)
        """
        return str(self.num)

class Holidays(models.Model):
    content = models.TextField('', max_length=200)

    def __str__(self):
        """
        Строка для представления модели в удобочитаемом имени (in Admin site etc.)
        """
        return '%s %s' % (str(self.id), 'день')
