from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import *

from .ssh_functions import ssh_send

# devices

@login_required
def list_devices(request):
  devices = Device.objects.all()
  return render(request, "device_and_screen_management/devices/list.html", {"devices": devices})

@login_required
def view_device(request, device_id):
  device = Device.objects.get(id=device_id)
  return render(request, "device_and_screen_management/devices/view.html", {"device": device})

@login_required
def restart_device(request, device_id):
  device = Device.objects.get(id=device_id)
  if device.host_ip and device.ssh_private_key:
    ssh_send(device.host_ip, device.ssh_private_key, "reboot")
    return redirect("view_device", device_id=device_id)
  return render(request, "errors/400.html", status=400)


# screens

@login_required
def list_screens(request):
  screens = Screen.objects.all()
  return render(request, "device_and_screen_management/screens/list.html", {"screens": screens})

@login_required
def view_screen(request, screen_id):
  screen = Screen.objects.get(id=screen_id)
  if request.POST:
    new_order = request.POST["new_order"].split(",") # [1, 2, 3]
    for slideshow_id in new_order:
      screen_slideshows = screen.slideshow_schedules.filter(slideshow_id=slideshow_id)
      for screen_slideshow in screen_slideshows:
        screen_slideshow.screen_slideshow_order = new_order.index(slideshow_id) + 1
        screen_slideshow.save()
    return redirect("view_screen", screen_id=screen_id)

  return render(request, "device_and_screen_management/screens/view.html", {"screen": screen})
