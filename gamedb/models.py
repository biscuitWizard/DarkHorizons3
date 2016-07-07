from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ItemCategory(models.Model):
    db_name = models.CharField(max_length=32)

class Item(models.Model):
    db_category = models.ForeignKey(ItemCategory)
    db_name = models.CharField(max_length=64)
    db_size_class = models.IntegerField()
    db_relative_size_class = models.IntegerField()
    db_weight_class = models.IntegerField()
    db_value = models.IntegerField()
    db_black_market_index = models.IntegerField()
    db_tags = models.CharField(max_length=512)


