from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from apps.device_and_screen_management.models import Screen
from apps.schedules.models import TimeSchedule, ScreenSlideshowSchedule

from .models import *


# assets

@login_required
def list_assets(request): # also used for new assets
  if request.POST:
    existing_asset = Asset.objects.filter(name=request.POST["name"])
    if existing_asset: return render(request, "errors/400.html", status=400)

    asset = Asset(name=request.POST["name"])
    asset.save()
    asset_version = AssetVersion(asset=asset, file=request.FILES["file"], created_by=request.user)
    asset_version.save()
    return redirect("list_assets")

  assets = Asset.objects.all()
  return render(request, "content_garage/assets/list.html", {"assets": assets})

@login_required
def view_asset(request, asset_id): # also used to update the asset
  if request.POST:
    asset = Asset.objects.get(id=asset_id)
    asset_version = AssetVersion(asset=asset, file=request.FILES["file"], created_by=request.user)
    asset_version.save()
    return redirect("view_asset", asset_id=asset_id)

  asset = Asset.objects.get(id=asset_id)
  return render(request, "content_garage/assets/view.html", {"asset": asset})

@login_required
def delete_asset(request, asset_id):
  asset = Asset.objects.get(id=asset_id)
  asset.delete()
  return redirect("list_assets")


# slideshows and slides

@login_required
def list_slideshows(request):
  slideshows = Slideshow.objects.all()
  return render(request, "content_garage/slideshows/list.html", {"slideshows": slideshows})

@login_required
def view_slideshow(request, slideshow_id):
  slideshow = Slideshow.objects.get(id=slideshow_id)
  if request.POST:
    match request.POST["type"]:
      case "order":
        new_order = request.POST["new_order"].split(",") # [1, 2, 3]
        for slide_id in new_order:
          slide = Slide.objects.get(id=slide_id)
          slide.order = new_order.index(slide_id) + 1
          slide.save()
      case "add_s3":
        screen = Screen.objects.get(id=request.POST["screen"])
        schedule = TimeSchedule.objects.get(id=request.POST["schedule"])
        existing_s3 = ScreenSlideshowSchedule.objects.filter(screen=screen, slideshow=slideshow, schedule=schedule)
        if not existing_s3:
          existing_s3_for_screen = ScreenSlideshowSchedule.objects.filter(screen=screen)
          new_s3 = ScreenSlideshowSchedule(screen=screen, slideshow=slideshow, schedule=schedule, screen_slideshow_order=existing_s3_for_screen.count() + 1)
          new_s3.save()
        else: existing_s3.delete()
      case "change_background":
        slideshow.background = request.POST["background"] if request.POST["background"] != "null" else None
        slideshow.save()
      case _: return render(request, "errors/400.html", status=400)
    return redirect("view_slideshow", slideshow_id=slideshow_id)

  screens = Screen.objects.all()
  schedules = TimeSchedule.objects.all()
  backgrounds = [[background.value, background.label] for background in Background]
  return render(request, "content_garage/slideshows/view.html", {"slideshow": slideshow, "screens": screens, "schedules": schedules, "backgrounds": backgrounds})

@login_required
def view_slide(request, slideshow_id, slide_id):
  slideshow = Slideshow.objects.get(id=slideshow_id)
  slide = Slide.objects.get(id=slide_id)
  if slide.slideshow != slideshow: return render(request, "errors/400.html", status=400)
  if request.POST:
    template_data = {}
    for key in request.POST:
      if key[:5] == "data-": template_data[key[5:]] = request.POST[key]
    slide.name = request.POST["name"]
    slide.duration = request.POST["duration"]
    slide.template_data = template_data
    slide.background = request.POST["background"]
    slide.save()
    return redirect("view_slide", slideshow_id=slideshow_id, slide_id=slide.id)
  backgrounds = [[background.value, background.label] for background in Background]
  return render(request, "content_garage/slideshows/slides/view.html", {"slideshow": slideshow, "slide": slide, "slide_template_properties": render_to_string(f"content_garage/slideshows/slides/properties/{slide.template}.html", { "slide": slide }), "backgrounds": backgrounds})

@login_required
def new_slide_select(request, slideshow_id):
  slideshow = Slideshow.objects.get(id=slideshow_id)
  # convert SlideTemplate into a list of [value, human name]
  slide_templates = [[template.value, template.label] for template in SlideTemplate]
  return render(request, "content_garage/slideshows/slides/new_select.html", {"slideshow": slideshow, "slide_templates": slide_templates})

@login_required
def new_slide(request, slideshow_id, slide_template_name):
  slideshow = Slideshow.objects.get(id=slideshow_id)
  if request.POST:
    template_data = {}
    for key in request.POST:
      if key[:5] == "data-": template_data[key[5:]] = request.POST[key]
    slide = Slide(
      name=request.POST["name"],
      slideshow=slideshow,
      duration=request.POST["duration"],
      template=slide_template_name,
      template_data=template_data,
      background=request.POST["background"],
      order=slideshow.slides.count() + 1,
    )
    slide.save()
    return redirect("view_slide", slideshow_id=slideshow_id, slide_id=slide.id)
  backgrounds = [[background.value, background.label] for background in Background]
  try: return render(request, "content_garage/slideshows/slides/new.html", {"slideshow": slideshow, "slide_template_name": next(template.label for template in SlideTemplate if template.value == slide_template_name), "slide_template_properties": render_to_string(f"content_garage/slideshows/slides/properties/{slide_template_name}.html"), "backgrounds": backgrounds})
  except: return render(request, "errors/404.html", status=404)

@login_required
def delete_slide(request, slideshow_id, slide_id):
  slide = Slide.objects.get(id=slide_id)
  if slide.slideshow.id != slideshow_id: return render(request, "errors/400.html", status=400)
  slide.delete()
  return redirect("view_slideshow", slideshow_id=slideshow_id)
