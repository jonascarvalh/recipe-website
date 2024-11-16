from django.shortcuts import render, get_object_or_404
from django.http import Http404
from recipes.models import Recipe
from django.db.models import Q
from utils.pagination import make_pagination
from django.views.generic import ListView
import os 
# HTTP REQUEST <- HTTP RESPONSE
# HTTP Request

PER_PAGE = int(os.environ.get('PER_PAGE', 9))

class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, 
            ctx.get('recipes'), 
            PER_PAGE
        )
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range
        })
        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
            is_published=True
        )

        if not qs:
            raise Http404()
        
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'title': f'{ctx.get('recipes')[0].category.name} - Category'
        })
        return ctx

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    
    def get_queryset(self, *args, **kwargs):
        self.search_term = self.request.GET.get('q', '').strip()

        if not self.search_term:
            raise Http404()
        
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=self.search_term) | # "OR" in database
                Q(description__icontains=self.search_term),
            ),
            is_published=True
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)        
        ctx.update({
            'search_term': self.search_term,
            'page_title': f'Search for "{self.search_term}"',
            'additional_url_query': f'&q={self.search_term}'
        })
        return ctx

def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published=True
    ).order_by('-id').first()
    recipe = get_object_or_404(Recipe, pk=id,is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True
    })