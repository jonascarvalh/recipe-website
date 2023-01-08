from django.shortcuts import render
from django.http import HttpResponse

# HTTP REQUEST <- HTTP RESPONSE
# HTTP Request

# Create your views here.
def home(request):
    return render(request, 'recipes/home.html', context={
        'name':'Jonas Carvalho'
    })
    #return HTTP response

def sobre(request):
    return HttpResponse('SOBRE.')
    #return HTTP response
    
def contato(request):
    return HttpResponse('CONTATO.')
    #return HTTP response