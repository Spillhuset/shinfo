from . import views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
  path("", views.index, name="index"),
  path("docs", views.docs, name="docs"),
  path("garage/", include("apps.content_garage.urls"), name="garage"),
  path("dasm/", include("apps.device_and_screen_management.urls"), name="dasm"),
  path("schedules/", include("apps.schedules.urls"), name="schedules"),
  path("viewer/", include("apps.viewer.urls"), name="viewer"),
]
