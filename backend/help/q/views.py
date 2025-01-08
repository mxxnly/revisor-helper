
from django.shortcuts import redirect, render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Shop
from .forms import ShopForm
from django.contrib.auth.decorators import login_required
from decorators import group_required

@login_required
def shop_list(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    shops = Shop.objects.all()
    form = ShopForm()
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()
    else:
        is_admin = False
    if 'Mobile' in user_agent:
        return render(request, 'mobile_shop_list.html', {'shops': shops, 'form': form, 'is_admin':is_admin})
    else:
        return render(request, 'q.html', {'shops': shops, 'form': form,'is_admin':is_admin})



@csrf_exempt
@group_required('Admin', 'God')
def reorder_shops(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data['order']:
            Shop.objects.filter(id=item['id']).update(position=item['position'])
        return JsonResponse({'status': 'ok'})
    


@group_required('Admin', 'God')
def shop_add(request):
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm()
    return render(request, 'q.html', {'form': form})
@group_required('Admin', 'God')
def shop_edit(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_list')
    else:
        form = ShopForm(instance=shop)
    return render(request, 'q.html', {'form': form})
@group_required('Admin', 'God')
def shop_delete(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    if request.method == 'POST':
        shop.delete()
        return redirect('shop_list')
    return render(request, 'q.html', {'shop': shop})