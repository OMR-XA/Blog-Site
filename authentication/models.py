from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from datetime import date

# Ensure User model is referenced correctly
User = settings.AUTH_USER_MODEL

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.SlugField(unique=True, max_length=255, null=False)
    birthday = models.DateField(auto_now_add=False, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pic = models.ImageField(upload_to='image/', null=True, blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name = 'friends_of')

class BlogPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=10000, null=False)
    publish = models.BooleanField(null=False, default=False)
    pic = models.ImageField(upload_to='image/', null=True, blank=True)
    date = models.DateField(auto_now_add=False, null=True)
    time = models.TimeField(auto_now_add=False, null=True)
    slug = models.SlugField(unique=True, null=False)

    class Meta:
        ordering = ['-pk', 'date']
        

class Comment(models.Model):
    bp = models.ForeignKey(BlogPost, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000, null=False)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    pic = models.ImageField(upload_to='image/', null=True, blank=True)
    
    class Meta:
        ordering = ['-pk', 'date']
    
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()
        if not self.time:
            self.time = timezone.now().time()
        super().save(*args, **kwargs)

class UserSettings(models.Model):
    PVC = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Friends Only'),
    ]
    
    APC = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    Theme = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('blue', 'Blue'),
    ]
    
    Language = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('ar', 'Arabic')
    ]
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=False)
    notifications = models.BooleanField(default=False)
    posts_visibility = models.CharField(max_length=100, choices=PVC, default='public')
    account_privacy = models.CharField(max_length=100, choices=APC, default='public')
    theme = models.CharField(max_length=100, choices=Theme, default='dark')
    language = models.CharField(max_length=100, choices=Language, default='en')