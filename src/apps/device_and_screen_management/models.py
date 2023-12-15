from django.db import models

from apps.viewer.models import Background

from datetime import timedelta
from django.utils import timezone

class Device(models.Model):
  name = models.CharField(max_length=32)
  enabled = models.BooleanField(default=False)
  host_ip = models.GenericIPAddressField(null=True, blank=True)
  ssh_private_key = models.TextField(null=True, blank=True)

  @property
  def pulsing(self): return self.enabled and any(screen.pulsing for screen in self.screens.all())

  def __str__(self): return f'{self.name} ({"aktiv" if self.enabled else "inaktiv"})'

  class Meta:
    ordering = ['name']
    permissions = (
      ('restart_device', 'Can restart device'),
      ('restart_device_service', 'Can restart device service'),
      ('restart_all_pages_for_device', 'Can restart all pages for device'),
    )

class Screen(models.Model):
  name = models.CharField(max_length=32)
  enabled = models.BooleanField(default=True)
  device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=True, null=True, related_name='screens')
  background = models.CharField(max_length=64, choices=Background.choices, default=Background.NO_BACKGROUND, blank=True)

  last_pulse = models.DateTimeField(blank=True, null=True)

  @property
  def pulsing(self): return self.enabled and self.last_pulse and self.last_pulse > timezone.now() - timedelta(seconds=30)

  def __str__(self): return self.name

  class Meta:
    ordering = ['device', 'name']
    permissions = (
      ('restart_page', 'Can restart page'),
    )
