from django.db.models.signals import post_save,post_delete
from .models  import Profile
from django.contrib.auth.models import User
from django.core.mail import  send_mail
from django.conf import  settings


def created(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            name=user.first_name,
            email=user.email
        )
        subject="LEAMC"
        body="it's my time"

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )


def updateUser(sender, instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleted(sender,instance,**kwargs):
    user = instance.user
    user.delete()


post_save.connect(created,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleted,sender=Profile)