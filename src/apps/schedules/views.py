from django.shortcuts import render

from .models import TimeSchedule

def list_schedules(request):
  schedules = TimeSchedule.objects.all()
  return render(request, 'schedules/list.html', {'schedules': schedules})
