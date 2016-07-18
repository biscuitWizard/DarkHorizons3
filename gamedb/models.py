from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HitEffect(models.Model):
    db_body_part = models.CharField(max_length=16)
    db_damage_type = models.CharField(max_length=16)
    db_trigger_index = models.IntegerField()
    db_status_effect = models.CharField(max_length=32)
    db_status_duration = models.CharField(max_length=16)

class ItemCategory(models.Model):
    db_name = models.CharField(max_length=32)

class ItemPrototype(models.Model):
    db_category = models.ForeignKey(ItemCategory)
    db_name = models.CharField(max_length=64)
    db_size_class = models.IntegerField()
    db_relative_size_class = models.IntegerField()
    db_weight_class = models.IntegerField()
    db_tags = models.CharField(max_length=512)

class Item(models.Model):
    db_name = models.CharField(max_length=64)
    db_item_prototype = models.ForeignKey(ItemPrototype)
    db_value = models.IntegerField()
    db_black_market_index = models.IntegerField()
    db_tags = models.CharField(max_length=512)

    def get_tag(self, tag_key):
        if tag_key in self.db_tags:
            tags = self.db_tags.split(';')
        elif tag_key in self.db_item_prototype.db_tags:
            tags = self.db_item_prototype.db_tags.split(';')
        else:
            return None

        try:
            result = next(tag for tag in tags if tag.startswith(tag_key))
            args = result.split('=')

            return args[len(args) - 1]
        except StopIteration:
            return None

class Trait(models.Model):
    db_name = models.CharField(max_length=32)

class Race(models.Model):
    db_name = models.CharField(max_length=32)
    db_traits = models.ManyToManyField(Trait, through='RaceTrait')
    db_body_table = models.CharField(max_length=128)

class RaceTrait(models.Model):
    db_race = models.ForeignKey(Race)
    db_trait = models.ForeignKey(Trait)
    db_value = models.IntegerField()

class Class(models.Model):
    db_name = models.CharField(max_length=32)
    db_is_force_sensitive = models.BooleanField()
    db_traits = models.ManyToManyField(Trait, through='ClassTrait')

class ClassTrait(models.Model):
    db_class = models.ForeignKey(Class)
    db_trait = models.ForeignKey(Trait)
    db_value = models.IntegerField()

class TraitWordlevel(models.Model):
    db_trait = models.ForeignKey(Trait)
    db_ordinal = models.IntegerField()
    db_value = models.CharField(max_length=32)

class CharacterLevel(models.Model):
    db_character_id = models.IntegerField()
    db_class = models.ForeignKey(Class)
    db_is_major_level = models.BooleanField()
    db_level_taken = models.IntegerField()

class BankAccount(models.Model):
    db_owner_id = models.IntegerField()
    db_credits = models.IntegerField()

class VehicleClass(models.Model):
    db_class_type = models.IntegerField()
    db_name = models.CharField(max_length=32)
    db_size_class = models.IntegerField()
    db_relative_size_class = models.IntegerField()
    db_weight_class = models.IntegerField()
    db_part_size_class = models.IntegerField()
