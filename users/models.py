from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} | Админ: {self.is_superuser}'


class Wallet(models.Model):
    name = models.CharField(max_length=50, default='Основной счет')
    currency = models.CharField(max_length=5, default='USD')
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    target = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.name} / {self.currency} | Основной: {self.target}'



    


