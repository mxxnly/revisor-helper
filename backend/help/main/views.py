from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Revisor
from django.db.models import F
from .forms import RevisorForm


def index(request):
    revisors = Revisor.objects.annotate(
        total_shops=F('shops') + F('way_shops') + F('move_shops')
    ).order_by('-total_shops')
    form = RevisorForm() 
    context = {
        'revisors': revisors, 
        'form': form,
    }
    return render(request, 'index.html', context)

def delete_revisor(request, revisor_id):

    revisor = get_object_or_404(Revisor, id=revisor_id)
    
    if request.method == "POST":
        revisor.delete()
        return redirect('home')  
    
    context = {
        'revisor': revisor,
    }
    return render(request, 'index.html', context)


def add_revisor(request):
    if request.method == "POST":
        form = RevisorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RevisorForm()
    return render(request, 'index.html', {'form': form})
    
def update_revisor(request, revisor_id, attr):
    revisor = get_object_or_404(Revisor, id=revisor_id)
    if request.method == "POST":
        current_value = getattr(revisor, attr, 0)
        current_value += 1
        setattr(revisor, attr, current_value)
        revisor.save()
        return redirect('home')


def add_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'shops')

def add_way_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'way_shops')

def add_move_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'move_shops')




