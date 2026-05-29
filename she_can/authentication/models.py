from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class people(AbstractUser):
    class Role(models.TextChoices):
       ADMIN = "ADMIN" , 'admin'
       USER = "USER", 'user'
       
    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices = Role.choices)
    
    def save(self, *args, **kwargs):
        if not self.pk :
            self.role = self.base_role
            return super().save(*args, **kwargs)
        
class NormalUser(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        all_user =  super().get_queryset(*args, **kwargs)
        return all_user.filter(role=people.Role.USER)

class user(people):
    base_role = people.Role.USER
    user = NormalUser()
    class Meta:
        proxy = True
        
    def welcome(self):
        return "Welcome to SHeCan Foundation"
    
@receiver(post_save, sender=user)
def create_normaluser_profile(sender, instance, created, **kwargs):
    if created and instance.role == "USER":
        NormalUserProfile.objects.create(user=instance)
        
    
    
class NormalUserProfile(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    name = models.CharField(True)
    age = models.IntegerField(null = True, blank=True)


    