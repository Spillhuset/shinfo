from django.urls import path

from . import views

urlpatterns = [
  # assets
  path("assets", views.list_assets, name="list_assets"),
  path("assets/<int:asset_id>", views.view_asset, name="view_asset"),
  path("assets/<int:asset_id>/delete", views.delete_asset, name="delete_asset"),
  # slideshows
  path("slideshows", views.list_slideshows, name="list_slideshows"),
  path("slideshows/<int:slideshow_id>", views.view_slideshow, name="view_slideshow"),
  ## slides
  path("slideshows/<int:slideshow_id>/slides/<int:slide_id>", views.view_slide, name="view_slide"),
  path("slideshows/<int:slideshow_id>/slides/<int:slide_id>/delete", views.delete_slide, name="delete_slide"),
  path("slideshows/<int:slideshow_id>/slides/new", views.new_slide_select, name="new_slide_select"),
  path("slideshows/<int:slideshow_id>/slides/new/<str:slide_template_name>", views.new_slide, name="new_slide"),
]
