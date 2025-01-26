# myapp/signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginActivity
from django.db.models.signals import post_save
from .models import Achievement
#from .utils import generate_certificate






@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    LoginActivity.objects.create(user=user, email=user.email, ip_address=ip)


#@receiver(post_save, sender=Achievement)

# def cre
# ate_achievement_certificate(sender, instance, created, **kwargs):
#     if created:
#         generate_certificate(instance)