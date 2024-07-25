
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Shop

def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'q.html', {'shops': shops})



@csrf_exempt
def reorder_shops(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data['order']:
            Shop.objects.filter(id=item['id']).update(position=item['position'])
        return JsonResponse({'status': 'ok'})