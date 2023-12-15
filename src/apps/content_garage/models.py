from django.db import models
from django.contrib.auth.models import User

import hashlib

from apps.viewer.models import Background

def hash_file(file):
  sha256 = hashlib.sha256()
  for chunk in file.chunks(): sha256.update(chunk)
  return sha256.hexdigest()

def hash_upload_to(instance, filename):
  # converts this: image.png, into this: image.1234abcd.png
  return f'assets/{filename.split(".")[0]}.{hash_file(instance.file)[:8]}.{filename.split(".")[-1]}'

class Asset(models.Model):
  name = models.CharField(max_length=32, unique=True)

  @property
  def current(self): return self.version_log.order_by('-created_at').first()

  def __str__(self): return self.name

  class Meta:
    ordering = ['name']

class AssetVersion(models.Model):
  asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='version_log')
  file = models.FileField(upload_to=hash_upload_to)
  created_at = models.DateTimeField(auto_now_add=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asset_version_logs')

  @property
  def file_html_tag(self):
    extension = self.file.name.split(".")[-1]
    if extension in ["jpg", "jpeg", "png", "gif", "svg", "webp"]: return "image"
    if extension in ["mp4", "webm", "ogg", "mp3", "wav", "flac", "aac", "opus"]: return "video"
    return "unknown"

  def __str__(self): return f'{self.asset.name}, {self.created_at}'

  class Meta:
    ordering = ['asset', '-created_at']

class Slideshow(models.Model):
  name = models.CharField(max_length=32)
  background = models.CharField(max_length=64, choices=Background.choices, blank=True, null=True)

  def __str__(self): return self.name

  class Meta:
    ordering = ['name']

class SlideTemplate(models.TextChoices):
  TEXT = "text", "Tekst"
  IMAGE = "image", "Bilde i fullskjerm"
  IMAGE_WITH_TEXT = "imagetext", "Bilde med tekst"
  IMAGE_BEHIND_TEXT = "imagebehindtext", "Bilde bak tekst"
  VIDEO = "video", "Video"
  IFRAME = "iframe", "Nettside (iframe)"
  CLOCK = "clock", "Klokke"

class Slide(models.Model):
  name = models.CharField(max_length=32)
  enabled = models.BooleanField(default=True)
  slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE, related_name='slides')
  duration = models.IntegerField(default=10)
  template = models.CharField(max_length=64, choices=SlideTemplate.choices)
  template_data = models.JSONField()
  background = models.CharField(max_length=64, choices=Background.choices, blank=True, null=True)
  order = models.PositiveSmallIntegerField()

  def __str__(self): return f'{self.slideshow}, #{self.order}: {self.name}'

  class Meta:
    ordering = ['slideshow', 'order']
