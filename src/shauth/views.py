from django.shortcuts import redirect
from jwt import decode
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

def auth(request):
    token = request.GET.get("shauth")

    if token:
        try:
          decoded = decode(token, settings.SHAUTH_ENCRYPTION_KEY, algorithms=["HS256"])
          if decoded:
              users = User.objects.filter(username=decoded["id"])
              if users: user = users[0]
              else: user = User.objects.create_user(decoded["id"])
              user.first_name = decoded["name"]
              apply_groups(user, decoded["userFlags"])
              user.save()
              login(request, user, backend="django.contrib.auth.backends.ModelBackend")
              return redirect("/")
        except Exception as e:
          print("Exception from SHauth:", e)
          pass

    return redirect("https://shauth.but-it-actually.works/?state=" + settings.SHAUTH_SYSTEM_NAME);

def apply_groups(user, flags):
  user.groups.clear()
  if flags & 1 <<  0: add_group_if_exists(user, "Crew")
  if flags & 1 <<  1: add_group_if_exists(user, "Nøkkel")
  if flags & 1 <<  2: add_group_if_exists(user, "Rådgiver")
  if flags & 1 <<  3: add_group_if_exists(user, "Leder")
  if flags & 1 <<  4: add_group_if_exists(user, "Event")
  if flags & 1 <<  5: add_group_if_exists(user, "Event Leder")
  if flags & 1 <<  6: add_group_if_exists(user, "PR")
  if flags & 1 <<  7: add_group_if_exists(user, "PR Leder")
  if flags & 1 <<  8: add_group_if_exists(user, "Streaming")
  if flags & 1 <<  9: add_group_if_exists(user, "Streaming Leder")
  if flags & 1 << 10: add_group_if_exists(user, "HR")
  if flags & 1 << 11: add_group_if_exists(user, "Systemstøtte")
  if flags & 1 << 12: add_group_if_exists(user, "Styre")
  if flags & 1 << 13: add_group_if_exists(user, "Styre Leder")

def add_group_if_exists(user, group):
  groups = Group.objects.filter(name=group)
  if groups: user.groups.add(groups[0])
