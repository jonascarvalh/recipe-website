from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe

from .forms import RegisterForm, LoginForm, AuthorRecipeForm

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)  
    return render(
        request, 
        'authors/pages/register_view.html', {
            'form': form,
            'form_action': reverse('authors:register_create'),
        }
    )

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password) # encrypt password
        user.save()

        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    
    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')
    
    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, "Invalid logout request")
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, "Invalid logout user")
        return redirect(reverse('authors:login'))
    
    messages.success(request, "Logged out successfully")
    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request, 
        "authors/pages/dashboard.html",
        {
            "recipes": recipes
        }
    )

@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not recipe:
        raise Http404()
    
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        # Garantias para salvar o form com segurança
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, "Sua receita foi salva com sucesso.")
        return redirect(reverse("authors:dashboard_recipe_edit", args=(id,)))
    
    return render(
        request, 
        "authors/pages/dashboard_recipe.html",
        {
            "form": form
        }
    )

@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_create_view(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        # Garantias para salvar o form com segurança
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        form.save()
        messages.success(request, "Sua receita foi salva com sucesso.")
        
        return redirect(reverse("authors:dashboard_recipe_edit", args=(recipe.pk,)))


    return render(
        request,
        "authors/pages/dashboard_recipe.html",
        {
            "form": form,
            "form_action": reverse("authors:dashboard_recipe_create_view")
        }
    )

@login_required(login_url="authors:login", redirect_field_name="next")
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    id = POST.get("id")
    
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()

    if not recipe:
        raise Http404()
    
    recipe.delete()
    messages.success(request, "Deleted succesfully")
    return redirect(reverse("authors:dashboard"))