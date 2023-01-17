from django.shortcuts import render
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipe
# HTTP REQUEST <- HTTP RESPONSE
# HTTP Request

# Create your views here.
def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)]
    })

def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True
    })
