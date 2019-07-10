from django.db import models

# Create your models here.


class Counter(models.Model):
    quantity = models.PositiveIntegerField('数量', default=0)