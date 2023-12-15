from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import json

from apps.content_garage.models import Slideshow, Slide

def send_slideshow_data(slideshow_id):
  channel_layer = get_channel_layer()
  slideshow = Slideshow.objects.get(id=slideshow_id)
  async_to_sync(channel_layer.group_send)(f'slideshow_{slideshow.id}', {
    "type": "send_data",
    "data": json.dumps({
      "type": "update_slideshow",
      "slideshow": {
        "id": slideshow.id,
        "background": slideshow.background,
        "slides": [{
          "id": slide.id,
          "duration": slide.duration,
          "html": render_to_string(f'viewer/slides/{slide.template}.html', { "data": slide.template_data }),
          "background": slide.background if slide.background != "null" else None,
        } for slide in slideshow.slides.all().order_by('order')]
      }
    })
  })

@receiver(post_save, sender=Slideshow)
def post_save_slideshow(sender, instance, **kwargs): send_slideshow_data(instance.id)

@receiver(post_save, sender=Slide)
def post_save_slide(sender, instance, **kwargs):
  if instance.slideshow: send_slideshow_data(instance.slideshow.id)

@receiver(post_delete, sender=Slide)
def post_delete_slide(sender, instance, **kwargs):
  if instance.slideshow: send_slideshow_data(instance.slideshow.id)
