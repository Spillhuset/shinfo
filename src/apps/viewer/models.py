from django.db import models


class Background(models.TextChoices):
  NO_BACKGROUND = "empty", "Blank bakgrunn"
  SPILLHUSET_DOWN_RIGHT = "shdownright", "Spillhuset logo nede til høyre"
  SPILLHUSET_DVD = "shdvd", "Spillhuset DVD logo"
  SPILLHUSET_DVD_DARKENED = "shdvddark", "Spillhuset DVD logo men litt mørkere"

  __empty__ = "Ingen (arver fra forelder)"
