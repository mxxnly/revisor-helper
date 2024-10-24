from django.shortcuts import render, redirect, get_object_or_404
from .models import Revisor
from django.http import HttpResponseBadRequest
from django.db.models import F
from .forms import RevisorForm
from django.contrib.auth.decorators import login_required
from decorators import group_required
from django.contrib.auth.models import User
from .models import Shop, Photo, Video
from .forms import PhotoForm, VideoForm
def welcome(request):
    if request.user.is_authenticated: 
        return render(request, 'home.html')
    else:
        return render(request, 'welcome.html')
      
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def revisor(request):
    revisors = Revisor.objects.annotate(
        total_shops=F('shops') + F('way_shops') + F('move_shops')
    ).order_by('-total_shops')
    form = RevisorForm() 
    context = {
        'revisors': revisors, 
        'form': form,
    }
    return render(request, 'revisor.html', context)

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


def shop_media_view(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    if request.method == 'POST':
        # Handle photo uploads
        photo_files = request.FILES.getlist('photos')
        for file in photo_files:
            Photo.objects.create(shop=shop, image=file)

        # Handle video uploads
        video_files = request.FILES.getlist('videos')
        for file in video_files:
            Video.objects.create(shop=shop, video_file=file)

        # Handle deletion
        if 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            if photo_id:
                photo = get_object_or_404(Photo, id=photo_id)
                photo.delete()

        if 'delete_video' in request.POST:
            video_id = request.POST.get('video_id')
            if video_id:
                video = get_object_or_404(Video, id=video_id)
                video.delete()

        return redirect('shop_media', shop_id=shop.id)

    photos = shop.photos.all()
    videos = shop.videos.all()

    return render(request, 'shop_media.html', {
        'shop': shop,
        'photos': photos,
        'videos': videos
    })