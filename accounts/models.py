from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, null = True, default = None)
    profile_name = models.CharField(max_length = 24, blank = True, null = True, default = None)
    phone_number = PhoneNumberField(blank=True, null = True, default = None)

    def __str__(self):
        return "%s %s" %(self.profile_name, self.phone_number)

    def save(self, *args, **kwargs):
        if self.user:
            self.profile_name = self.user.first_name
        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender = User)
