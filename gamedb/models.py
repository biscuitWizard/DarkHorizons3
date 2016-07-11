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

class Trait(models.Model):
    db_name = models.CharField(max_length=32)

class Race(models.Model):
    db_name = models.CharField(max_length=32)

class RaceTrait(models.Model):
    db_race = models.ForeignKey(Race)
    db_trait = models.ForeignKey(Trait)
    db_value = models.IntegerField()

class Class(models.Model):
    db_name = models.CharField(max_length=32)
    db_is_force_sensitive = models.BooleanField()

class ClassTraits(models.Model):
    db_class = models.ForeignKey(Class)
    db_trait = models.ForeignKey(Trait)
    db_value = models.IntegerField()

class TraitWordlevel(models.Model):
    db_trait = models.ForeignKey(Trait)
    db_ordinal = models.IntegerField()
    db_value = models.CharField(max_length=32)