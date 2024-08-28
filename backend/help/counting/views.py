from django.shortcuts import render, redirect
from .forms import WorkLogForm
from .models import WorkLog
from django.utils import timezone
import calendar
from django.contrib.auth.decorators import login_required

@login_required
def work_log_view(request):
    if request.method == 'POST':
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.user = request.user
            existing_log = WorkLog.objects.filter(
                user=work_log.user,
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

    work_logs = WorkLog.objects.filter(date__year=year, date__month=month, user=request.user)

    context = {
        'form': form,
        'calendar': cal,
        'year': year,
        'month': month,
        'work_logs': work_logs,
    }
    return render(request, 'calendar.html', context)
    
@login_required
def delete_work_log(request, log_id):
    if request.method == 'POST':
        log = WorkLog.objects.filter(
            id=log_id,
            user=request.user
        ).first()

        if log:
            log.delete()

    return redirect('work_log')
