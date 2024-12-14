from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from decorators import group_required
from main.models import Revisor
from django.shortcuts import render, redirect
from django.http import JsonResponse

@login_required
@group_required('Admin', 'God')
def update_hours_difference(request):
    if request.method == 'POST':
        revisor_id = request.POST.get('revisor_id')
        hours_difference = request.POST.get('hours_difference')

        if revisor_id and hours_difference:
            try:
                revisor = Revisor.objects.get(id=revisor_id)
                revisor.plus_or_minus = hours_difference
                revisor.save()
                return redirect('salary_list')
            except Revisor.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Revisor does not exist'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        revisors = Revisor.objects.all()
        return render(request, 'difference.html', {'revisors': revisors})
    
    
