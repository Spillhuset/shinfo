from . import views
from django.urls import path

urlpatterns = [
  path("screens/<int:screen_id>", views.screen_viewer, name="screen_viewer"),
  path("slideshows/<int:slideshow_id>", views.slideshow_viewer, name="slideshow_viewer"),
  path("slides/<int:slide_id>", views.slide_viewer, name="slide_viewer"),
  path("backgrounds/<str:background_name>", views.background_viewer, name="background_viewer"),
  path("slide_templates/<str:slide_template_name>", views.slide_template_viewer, name="slide_template_viewer"),
]
