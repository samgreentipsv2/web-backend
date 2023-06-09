
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Plan(models.Model):
   name = models.CharField(blank=True, max_length=300)
   price = models.DecimalField(decimal_places=2, max_digits=9, default=0, blank=True, null=True)
   duration= models.DurationField( default=datetime.timedelta(weeks=1),blank=True, null=True)
   
     
   def __str__(self):
       return f" {self.name}" 
   

class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
        
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=55, blank=True, null=True)
    last_name = models.CharField(max_length=55, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False, verbose_name="is VIP")
    plan_sub = models.ForeignKey(Plan,on_delete=models.CASCADE, related_name="subscribed_to", blank=True, null=True, verbose_name="plan")
    day_subscribed = models.DateField(verbose_name="Subscription started", blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email

class Categorie(models.Model):
    category_name = models.CharField(verbose_name="vip_category", max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.category_name
    
    
class FreeCategorie(models.Model):
    category_name = models.CharField(verbose_name="free_category", max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.category_name
    
    
class FreeInplayOdd(models.Model):
    match= models.CharField(blank=True, max_length=300)
    prediction= models.CharField(blank=True, max_length=300)
    time = models.DateTimeField( blank=True, null=True)
    

class Game(models.Model):
    match= models.CharField(blank=True, max_length=300)
    category = models.ForeignKey(FreeCategorie, on_delete=models.CASCADE, related_name="free_categories",blank=True, null=True)
    prediction= models.CharField(blank=True, max_length=300, verbose_name='prediction')
    # odd =  models.DecimalField(decimal_places=2, max_digits=3, default=0, blank=True, null=True)
    league= models.CharField(blank=True, max_length=300)
    time = models.DateTimeField(blank=True, null=True)
    # is_betoftheday = models.BooleanField( default =False, blank=True, null=True)
    
    
    
    
    def __str__(self):
        return (f"{self.match}")
    
    
class FreePrediction(models.Model):
    games = models.ManyToManyField(Game, blank=True, related_name='freegames', verbose_name='Free Predictions')
    time = models.DateField( blank=True, null=True)
    

class DailyBet(models.Model):
    games = models.ManyToManyField(Game, blank=True, related_name='betoftheday', verbose_name='Bet Of The Day')
    time = models.DateField( blank=True, null=True)
    
    

    
    
class VipGame(models.Model):
    match= models.CharField(blank=True, max_length=300)
    Prediction= models.CharField(blank=True, max_length=300, verbose_name='prediction')
    odd =  models.DecimalField(decimal_places=2, max_digits=3, default=0, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="vip_categories" ,blank=True, null=True)
    
    

    
    
class VipOdd(models.Model):
    games = models.ManyToManyField(VipGame, blank=True, related_name='vip_games')
    total_odds = models.DecimalField(decimal_places=2, max_digits=3, default=0, blank=True, null=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="odds_categories" ,blank=True, null=True)
    betking_code = models.CharField(blank=True, max_length=30)
    onexbet_code = models.CharField(blank=True, max_length=30, verbose_name="1xbet code")
    twentytwobet_code = models.CharField(blank=True, max_length=30, verbose_name='22bet code')
    sportybet_code = models.CharField(blank=True, max_length=30)
    bet9ja_code = models.CharField(blank=True, max_length=30)
    Helabet_code = models.CharField(blank=True, max_length=30)
    date = models.DateField( null=True, blank=True)
    
    
    
class RecentVipResult(models.Model):
    status = models.BooleanField(default=False)
    day = models.DateField( null=True, blank=True)
    
    
    
    
class SubRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriber" ,blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan_subscribed" ,blank=True, null=True)
    day = models.DateField(null=True, blank=True, verbose_name="day_subscribed")
    
    
    def __str__(self):
        return (f"{self.user} subscribed to {self.plan} on {self.day}")
    
    
   

    


   
    


