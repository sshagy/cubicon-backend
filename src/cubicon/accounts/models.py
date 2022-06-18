from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # wca_id = models.CharField(primary_key=True, max_length=10)
    # name = models.CharField(max_length=80, blank=True)
    # email = models.EmailField(default='')
    # date_of_birth = models.DateField(auto_now=True)
    # gender = models.CharField(max_length=1, blank=True)
    # country = models.ForeignKey(Country, models.DO_NOTHING, default=None, null=True, blank=True)
    # manage_competitions = models.BooleanField(default=False)

    # TODO: connect to sotial web

    class Meta:
        verbose_name = 'User'

    def __str__(self):
        return f"Пользователь [ID={self.id}]: {self.username}"
