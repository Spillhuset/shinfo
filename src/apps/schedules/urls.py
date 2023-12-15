from . import views
from django.urls import path

urlpatterns = [
  path("", views.list_schedules, name="list_schedules"),
]
