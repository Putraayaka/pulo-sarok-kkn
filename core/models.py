from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """Extended user model for village staff"""
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    is_village_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.position}"


class UserProfile(models.Model):
    """Additional profile information for users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class UMKMBusiness(models.Model):
    """UMKM business data for WhatsApp bot integration"""
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    business_type = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.owner_name}"


class WhatsAppBotConfig(models.Model):
    """Configuration for WhatsApp bot integration"""
    bot_name = models.CharField(max_length=100)
    welcome_message = models.TextField()
    business_hours_start = models.TimeField()
    business_hours_end = models.TimeField()
    auto_reply_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bot Config: {self.bot_name}"


class SystemSettings(models.Model):
    """General system settings"""
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.setting_key}: {self.setting_value[:50]}"
