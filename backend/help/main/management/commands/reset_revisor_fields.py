from django.core.management.base import BaseCommand
from main.models import Revisor
from django.utils import timezone

class Command(BaseCommand):
    help = 'Resets shops, way_shops, and move_shops fields for all Revisors on the first day of the month'

    def handle(self, *args, **options):
        now = timezone.now()
        if now.day == 14:
            Revisors = Revisor.objects.all()
            for revisor in Revisors:
                revisor.shops = 0
                revisor.way_shops = 0
                revisor.move_shops = 0
                revisor.save()
            self.stdout.write(self.style.SUCCESS('Successfully reset fields for all Revisors.'))
        else:
            self.stdout.write(self.style.WARNING('Today is not the first day of the month.'))
