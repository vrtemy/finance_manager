from django.db import models


class ActiveCoin(models.Model):
    id_in_cmc = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)
    rank = models.PositiveSmallIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'id: {self.id} | id in cmc: {self.id_in_cmc} | {self.name} {self.symbol}'
