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
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)+"-"+self.title[:15]

class Piece(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    pId = models.IntegerField(default=1,blank=False,null=False);
    text = models.CharField(max_length=500)
    next = models.IntegerField(null=True, blank=True)
    
    objects = InheritanceManager()

    class Meta:
            unique_together = (("story", "pId"),)

    def __str__(self):
        return str(self.story)+" "+str(self.pId)+": "+self.text[:15]


class DecisionPiece(Piece):
    def __str__(self):
        return str(self.story)+" "+str(self.pId)+" (Decision)"

class ChoicePiece(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    decision = models.ForeignKey(DecisionPiece, null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    next = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.story)+" "+str(self.decision)+": "+self.text[:15]

class WinPiece(Piece):
    pass

class LosePiece(Piece):
    pass
