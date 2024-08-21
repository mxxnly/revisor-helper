from django.shortcuts import render, redirect
from .forms import WorkLogForm
from .models import WorkLog
from main.models import Revisor
from django.utils import timezone
import calendar
from django.contrib.auth.decorators import login_required

@login_required
def work_log_view(request):
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.revisor = request.user.revisor
            existing_log = WorkLog.objects.filter(
                revisor=work_log.revisor,
                date=work_log.date
            ).first()

            if existing_log:

                existing_log.delete()
                
            work_log.save()
            return redirect('work_log')
    else:
        form = WorkLogForm()

    today = timezone.now().date()
    year = today.year
    month = today.month
    cal = calendar.Calendar().monthdayscalendar(year, month)

    work_logs = WorkLog.objects.filter(revisor=request.user.revisor, date__year=year, date__month=month)

    context = {
        'form': form,
        'calendar': cal,
        'year': year,
        'month': month,
        'work_logs': work_logs,
    }
    return render(request, 'calendar.html', context)
    