from django.shortcuts import render, get_object_or_404, redirect
from .models import Rating
from main.models import Shop, Revisor
from .forms import RatingForm
from django.contrib.auth.decorators import login_required

@login_required
def rate_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    revisor = Revisor.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            ratings = form.cleaned_data
            Rating.objects.create(
                shop=shop,
                user=request.user,
                personal=ratings['personal'],
                purity=ratings['purity'],
                sorting=ratings['sorting']
            )
            shop.upd_avg_rating() 
            shop.upd_avg_ratings()
            if revisor:
                revisor.update_favourite_shop()
            return redirect('home')  
    else:
        form = RatingForm()

    return render(request, 'rate_shop.html', {'form': form, 'shop': shop})
