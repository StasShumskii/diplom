from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth import login


@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
