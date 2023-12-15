from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from datetime import datetime
from asgiref.sync import async_to_sync

from apps.content_garage.models import Slideshow
from apps.device_and_screen_management.models import Screen
from apps.schedules.models import ScreenSlideshowSchedule

class ScreenConsumer(JsonWebsocketConsumer):
  def connect(self):
    self.screen_id = self.scope['url_route']['kwargs']['screen_id']
    try: screen = Screen.objects.get(id=self.screen_id)
    except Screen.DoesNotExist: return self.close()
    self.group_name = f'infoscreen_{self.screen_id}'
    async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
    self.real = self.scope['query_string'].decode('utf-8') == "real=true"
    if self.real: async_to_sync(self.channel_layer.group_add)(f'{self.group_name}_real', self.channel_name)
    self.accept()
    self.send_json({
      "type": "init",
      "screen": {
        "id": self.screen_id,
        "background": screen.background,
      }
    })

  def receive_json(self, json_data):
    screen = Screen.objects.get(id=self.screen_id)
    if json_data["type"] == "slideshow_done":
      try: current_s3 = ScreenSlideshowSchedule.objects.get(id=json_data["s3"]) if "s3" in json_data else None
      except ScreenSlideshowSchedule.DoesNotExist: current_s3 = None
      if current_s3: async_to_sync(self.channel_layer.group_discard)(f'slideshow_{current_s3.slideshow.id}', self.channel_name)
      active_s3 = [s3 for s3 in screen.slideshow_schedules.all().order_by('screen_slideshow_order') if s3.schedule.cron_active and s3.slideshow.slides.count() > 0]
      if active_s3:
        current_s3_order = current_s3.screen_slideshow_order if current_s3 else -1
        next_s3 = next((s3 for s3 in active_s3 if s3.screen_slideshow_order > current_s3_order), active_s3[0])
        self.send_json({
          "type": "run_slideshow",
          "s3": next_s3.id,
          "slideshow": {
            "id": next_s3.slideshow.id,
            "background": next_s3.slideshow.background,
            "slides": [{
              "id": slide.id,
              "duration": slide.duration,
              "html": render_to_string(f'viewer/slides/{slide.template}.html', { "data": slide.template_data }),
              "background": slide.background if slide.background != "null" else None,
            } for slide in next_s3.slideshow.slides.all().order_by('order')]
          }
        })
        async_to_sync(self.channel_layer.group_add)(f'slideshow_{next_s3.slideshow.id}', self.channel_name)
      else: self.send_json({ "type": "run_slideshow", "s3": None, "slideshow": None })

    if self.real:
      screen.last_pulse = datetime.now()
      screen.save()

  def send_data(self, event): self.send(text_data=event["data"])
  def disconnect(self, close_code): async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)


class SlideshowConsumer(JsonWebsocketConsumer):
  def connect(self):
    self.slideshow_id = self.scope['url_route']['kwargs']['slideshow_id']
    try: slideshow = Slideshow.objects.get(id=self.slideshow_id)
    except Slideshow.DoesNotExist: return self.close()
    self.group_name = f'slideshow_{self.slideshow_id}'
    async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
    self.accept()
    self.send_json({
      "type": "init",
      "slideshow": {
        "background": slideshow.background,
        "slides": [{
          "id": slide.id,
          "duration": slide.duration,
          "html": render_to_string(f'viewer/slides/{slide.template}.html', { "data": slide.template_data }),
          "background": slide.background if slide.background != "null" else None,
        } for slide in slideshow.slides.all().order_by('order')]
      }
    })

  def send_data(self, event): self.send(text_data=event["data"])
  def disconnect(self, close_code): async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
