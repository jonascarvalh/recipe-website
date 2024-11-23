from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from recipes.models import Recipe
from django.db.models import Q
from utils.pagination import make_pagination
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
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

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()
        return JsonResponse(
            list(recipes_list),
            safe=False
        )

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
            'title': ctx.get('recipes')[0].category.name + ' - Category'
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

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })
        return ctx
    
class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri(recipe.cover.url)
        else:
            recipe_dict['cover'] = ''

        del(recipe_dict['is_published'])
        del(recipe_dict['preparation_steps_is_html'])

        return JsonResponse(
            recipe_dict,
            safe=False
        )