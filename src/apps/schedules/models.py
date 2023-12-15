from django.db import models
from cron_validator import CronValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.content_garage.models import Slideshow
from apps.device_and_screen_management.models import Screen


def isCronValid(str):
  try: CronValidator.parse(str)
  except: raise ValidationError(f'"{str}" is not a valid cron expression')

class TimeSchedule(models.Model):
  name = models.CharField(max_length=32)
  cron = models.CharField(max_length=128, validators=[isCronValid])
  cron_is_reversed = models.BooleanField(default=False)
  cron_explanation = models.CharField(max_length=128)

  @property
  def cron_active(self):
    result = CronValidator.match_datetime(self.cron, timezone.now())
    return not result if self.cron_is_reversed else result

  def __str__(self): return f'{self.name} {"!" if self.cron_is_reversed else ""}({self.cron})'


class ScreenSlideshowSchedule(models.Model):
  screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="slideshow_schedules")
  slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE, related_name="screen_schedules")
  schedule = models.ForeignKey(TimeSchedule, on_delete=models.CASCADE, related_name="screen_slideshows")
  screen_slideshow_order = models.PositiveSmallIntegerField()

  def __str__(self): return f'{self.slideshow.name} på {self.screen} - {self.schedule}'
