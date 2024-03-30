from django.shortcuts import render, get_object_or_404
from .models import Cat


def index(request):
    cats = Cat.objects.all()
    return render(request, 'catshop/index.html', {'cats': cats})


def show_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    return render(request, 'catshop/show.html', {'cat': cat})


def about(request):
    return render(request, 'catshop/about.html')