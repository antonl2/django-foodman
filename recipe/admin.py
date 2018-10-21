from django.contrib import admin

# Register your models here.

from .models import Recipe, Unit, Ingredient, Recipe_ingredient

admin.site.register(Recipe)
admin.site.register(Unit)
admin.site.register(Ingredient)
admin.site.register(Recipe_ingredient)