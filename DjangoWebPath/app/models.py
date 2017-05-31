"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.managers import InheritanceManager

# Create your models here.

"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  
    instance.profile.save()"""
  
class Story(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)+"-"+self.title[:15]

class Piece(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    next = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    objects = InheritanceManager()

    def __str__(self):
        return str(self.story)+"-"+str(self.pk)+"-"+self.text[:15]

class DecisionPiece(Piece):
    pass

class ChoicePiece(Piece):
    decision = models.ForeignKey(DecisionPiece, null=True, blank=True, on_delete=models.CASCADE)

class WinPiece(Piece):
    pass

class LosePiece(Piece):
    pass
