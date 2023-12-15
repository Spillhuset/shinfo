from . import views
from django.urls import path

urlpatterns = [
  # devices
  path("devices", views.list_devices, name="list_devices"),
  path("devices/<int:device_id>", views.view_device, name="view_device"),
  path("devices/<int:device_id>/restart_all_pages", views.restart_all_pages_for_device, name="restart_all_pages_for_device"),
  path("devices/<int:device_id>/restart_service", views.restart_device_service, name="restart_device_service"),
  path("devices/<int:device_id>/restart", views.restart_device, name="restart_device"),

  # screens
  path("screens/", views.list_screens, name="list_screens"),
  path("screens/<int:screen_id>", views.view_screen, name="view_screen"),
]
