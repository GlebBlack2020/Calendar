from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

class Country(models.Model):
    country = models.TextField()

    def __str__(self):
        return self.country


class ProfileUser(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='user_country')


class CreateEvent(models.Model):
    CHOICE_TIME = [
        (timedelta(hours=1), "За час",),
        (timedelta(hours=2), "За 2 часа"),
        (timedelta(hours=4), "За 4 часа"),
        (timedelta(hours=24), "За день"),
        (timedelta(hours=168), "За неделю"),
    ]
    chose_time = CHOICE_TIME
    user_event = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="user",
                                   verbose_name="автор  события")
    title = models.CharField(max_length=100, verbose_name="название события")

    date_start = models.DateTimeField(verbose_name="Время начала события")
    date_finish = models.DateTimeField(blank=True, null=True, verbose_name="Время окончания события")
    reminder = models.CharField(max_length=40, verbose_name="Когда напомнить?", choices=chose_time,
                                null=True, blank=True)
    notification = models.BooleanField(verbose_name="Оповещение", default=False)


    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.date_finish is None:
            self.date_finish = self.date_start.replace(hour=23, minute=59, second=59)
        super().save(**kwargs)


class Holidays(models.Model):
    title = models.CharField(max_length=200, verbose_name="Праздник")
    holiday_start = models.DateTimeField(verbose_name="Начало праздника")
    holiday_finish = models.DateTimeField(verbose_name="Окончание праздника")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.title