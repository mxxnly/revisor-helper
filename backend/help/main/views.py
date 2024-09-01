from django.shortcuts import render, redirect, get_object_or_404
from .models import Revisor
from django.http import HttpResponseBadRequest
from django.db.models import F
from .forms import RevisorForm
from django.contrib.auth.decorators import login_required
from decorators import group_required
from django.contrib.auth.models import User
@login_required
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

@login_required
@group_required('Admin', 'God')
def delete_revisor(request, revisor_id):

    revisor = get_object_or_404(Revisor, id=revisor_id)
    
    if request.method == "POST":
        revisor.delete()
        return redirect('home')  
    
    context = {
        'revisor': revisor,
    }
    return render(request, 'index.html', context)

@login_required
@group_required('Admin', 'God')
def add_revisor(request):
    if request.method == "POST":
        form = RevisorForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()   
            new_revisor = form.save(commit=False)
            if user:
                new_revisor.user = user
            new_revisor.save()
            return redirect('home')
    else:
        form = RevisorForm()
    return render(request, 'index.html', {'form': form})
@login_required
@group_required('Admin', 'God')
def update_revisor(request, revisor_id, attr):
    revisor = get_object_or_404(Revisor, id=revisor_id)
    if request.method == "POST":
        current_value = getattr(revisor, attr, 0)
        current_value += 1
        setattr(revisor, attr, current_value)
        revisor.save()
        return redirect('home')

@login_required
@group_required('Admin', 'God')
def add_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'shops')
@login_required
@group_required('Admin', 'God')
def add_way_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'way_shops')
@login_required
@group_required('Admin', 'God')
def add_move_shops(request, revisor_id):
    return update_revisor(request, revisor_id, 'move_shops')




