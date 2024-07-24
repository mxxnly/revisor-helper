from django.shortcuts import render
from .models import Revisor

def index(request):
    revisors = Revisor.objects.all()  # Query all instances of the Revisor model
    context = {
        'revisors': revisors, 
    }
    return render(request, 'index.html', context)
