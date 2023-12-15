from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path("ws/screens/<int:screen_id>", consumers.ScreenConsumer.as_asgi()),
  path("ws/slideshows/<int:slideshow_id>", consumers.SlideshowConsumer.as_asgi()),
]
