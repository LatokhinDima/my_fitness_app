from django.shortcuts import render
from django.http import HttpResponse

def index(request) -> HttpResponse:
    context: dict[str, str] = {
        'title': "My fitness",
        'content': 'There will be a "My Fitness" app here!!!'
    }
    return render(request, 'fitness/index.html', context)
