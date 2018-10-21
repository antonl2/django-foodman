from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=250)

    def __str__(self):
        return self.recipe_name


class Unit(models.Model):
    unit_name = models.CharField(max_length=250)

    def __str__(self):
        return self.unit_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=250)
    unit_name =  models.ForeignKey(Unit, on_delete=models.CASCADE)
    unit_amount =  models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse('recipe:ingredient')

    def __str__(self):
        return self.ingredient_name


class Recipe_ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('recipe:index')
        # return reverse('recipe:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.recipe_id)
