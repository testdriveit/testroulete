from operator import mod
from django.db import models

# Create your models here.
class RouleteRounds(models.Model):
    round_id = models.IntegerField(null=True)
    lucky_number = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)


