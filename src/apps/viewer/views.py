from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse

from ..content_garage.models import Slideshow, Slide
from ..device_and_screen_management.models import Screen

@xframe_options_exempt
def screen_viewer(request, screen_id):
  try: screen = Screen.objects.get(id=screen_id)
  except Screen.DoesNotExist: return render(request, "errors/404.html", status=404)
  return render(request, "viewer/screen.html", { "screen": screen })

@xframe_options_exempt
def slideshow_viewer(request, slideshow_id):
  try: slideshow = Slideshow.objects.get(id=slideshow_id)
  except Slideshow.DoesNotExist: return render(request, "errors/404.html", status=404)
  return render(request, "viewer/slideshow.html", { "slideshow": slideshow })

@xframe_options_exempt
def slide_viewer(request, slide_id):
  try: slide = Slide.objects.get(id=slide_id)
  except Slide.DoesNotExist: return render(request, "errors/404.html", status=404)
  return render(request, "viewer/slide.html", { "slide": slide, "background_html_body": render_to_string(f'viewer/backgrounds/{slide.background if slide.background != None and slide.background != "null" else "empty"}.html'), "slide_html_body": render_to_string(f'viewer/slides/{slide.template}.html', { "data": slide.template_data }) })

@xframe_options_exempt
def background_viewer(request, background_name):
  try: background_html_body = render_to_string(f'viewer/backgrounds/{background_name}.html')
  except: return render(request, "errors/404.html", status=404)
  if request.GET.get("raw") == "true":
    return HttpResponse(background_html_body, content_type="text/plain")
  return render(request, "viewer/background.html", { "background_name": background_name, "background_html_body": background_html_body })

@xframe_options_exempt
def slide_template_viewer(request, slide_template_name):
  try: return render(request, "viewer/slide.html", { "slide": slide_template_name, "slide_html_body": render_to_string(f'viewer/slides/{slide_template_name}.html') })
  except: return render(request, "errors/404.html", status=404)
