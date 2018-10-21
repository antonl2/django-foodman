from django.urls import path, re_path
from . import views #. look in the same directory where we are
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'recipe'

urlpatterns = [
    # /recipe/
    re_path(r'^$', views.IndexView.as_view(), name='index'),

    # /recipe/<recipe_id>/
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # for deleting and updating views
    # recipe/recipe/add/
    re_path(r'^recipe/add/$', views.RecipeCreate.as_view(), name='recipe-add'),

    # # recipe/recipe/2/
    re_path(r'^recipe/(?P<pk>[0-9]+)/$', views.RecipeUpdate.as_view(), name='recipe-update'),

    # # recipe/recipe/add/
    re_path(r'^(?P<pk>[0-9]+)/delete/$', views.RecipeDelete.as_view(), name='recipe-delete'),

    # /recipe/ingredient/
    re_path(r'^ingredient/$', views.IngredientView.as_view(), name='ingredient'),

    # # recipe/ingredient/<ingredient_id>/
    re_path(r'^ingredient/(?P<pk>[0-9]+)/$', views.IngredientDetailView.as_view(), name='ingredient-detail'),

    # /recipe/ingredient/add
    re_path(r'^ingredient/add/$', views.IngredientCreate.as_view(), name='ingredient-add'),
    
    # # recipe/ingredient/2/
    re_path(r'^ingredient/(?P<pk>[0-9]+)/update', views.IngredientUpdate.as_view(), name='ingredient-update'),

    # # recipe/ingredient/2/delete
    re_path(r'^ingredient/(?P<pk>[0-9]+)/delete', views.IngredientDelete.as_view(), name='ingredient-delete'),

    # Others
    re_path(r'^get_recipes', views.get_recipes, name='recipe-search'),

    re_path(r'^get_ingredients', views.get_ingredients, name='ingredient-search'),
]
