from django.shortcuts import render
from .forms import UserForm
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect

# Create your views here.
def index(request):
    userform = UserForm()
    return render(request, "a545/index.html", {"form": userform})

def about(request):
    return HttpResponse("About")

def contact(request):
    return HttpResponseRedirect("/about")

def details(request):
    return HttpResponsePermanentRedirect("/")


def products(request, productid):
    category = request.GET.get("cat", "")
    output = "<h2>Продукт № {0} Категория: {1}</h2>" .format(productid, category)
    return HttpResponse(output)

def users(request):
    id = request.GET.get("id", 1)
    name = request.GET.get("name", "Максим")
    output = "<h2>Пользователь</h2><h3>id: {0} Имя: {1}</h3 >" .format(id, name)
    return HttpResponse(output)
