from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
# from django.urls import reverse
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import connection
from .models import Recipe, Ingredient, Unit, Recipe_ingredient

from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

class IndexView(generic.ListView):
    template_name='recipe/index.html'
    context_object_name = 'all_recipes'

    def get_queryset(self):
        return Recipe_ingredient.objects.order_by('recipe')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['raw_recipes'] = Recipe.objects.order_by('id')
        return context

class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipe/details.html'

    context_object_name = 'all_recipes'

    def get_queryset(self):
        return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        pkid = self.kwargs['pk']
        context = super(DetailView, self).get_context_data(**kwargs)
        query = """select recipe_id, ingredient_name, amount, unit_name, unit_amount, 
            round(cast(amount as float)/cast(unit_amount as float), 2) as cost from 
            ((select recipe_id, ingredient_name, amount, unit_id, unit_amount from 
            (select recipe_id, ingredient_id, amount, unit_id from recipe_recipe_ingredient) as A 
            left join 
            (select * from recipe_ingredient) as B on A.ingredient_id = B.id) as C
            left join
            (select * from recipe_unit) as D on C.unit_id = D.id) where recipe_id=""" + pkid
        with connection.cursor() as cursor:
            cursor.execute(query)
            ingredients = dictfetchall(cursor)
        total = 0
        for ingredient in ingredients:
            total += ingredient['cost']
    
        context['ingredients'] = ingredients
        context['total'] = total
        return context

class RecipeCreate(CreateView):
    model = Recipe_ingredient
    fields = ['recipe', 'ingredient', 'amount', 'unit']


class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['ingredient_name', 'unit_name', 'unit_amount']


class RecipeUpdate(UpdateView):
    model = Recipe_ingredient
    fields = ['recipe', 'ingredient', 'amount', 'unit']


class RecipeDelete(DeleteView):
    model = Recipe_ingredient
    success_url = reverse_lazy('recipe:index')

class IngredientView(generic.ListView):
    template_name='recipe/ingredient.html'
    context_object_name = 'ingredients'

    def get_queryset(self):
        return Ingredient.objects.all()

class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'recipe/ingredient_details.html'

    context_object_name = 'ingredients'

    def get_queryset(self):
        return Ingredient.objects.all()

class IngredientUpdate(UpdateView):
    model = Ingredient
    fields = ['ingredient_name', 'unit_name', 'unit_amount']

class IngredientDelete(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('recipe:ingredient')

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_recipes(request):
    print('done')

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, 'json'):
            return str(obj)
        return super().default(obj)

def get_ingredients(request):
    # if request.method == 'POST':
    #     str_search = request.POST.get('search', None)
    # else:
    #     str_search = 'Test'
    str_search = request.GET['search']
    # return HttpResponse(str_search)
    if str_search == '':
        data = Ingredient.objects.all()
    else:
        try:
            num_search = int('0' + str_search)
            data = Ingredient.objects.filter(pk=num_search)
            # data = Ingredient.objects.filter(Q(ingredient_name__contains=str_search) | Q(pk=num_search))
        except:
            data = Ingredient.objects.filter(ingredient_name__contains=str_search)
    
    return render(request, 'recipe/get_ingredients.html', {'ingredietns': data})