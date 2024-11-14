from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

import hashlib
# Create your models here.

# Custom User Manager
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Categories(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=Categories)
def categories_post_save(sender, instance, **kwargs):
    if instance._state.adding:
        if instance.parent is None:
            instance.parent_id = 1


class Products(models.Model):
    name = models.TextField(blank=False, null=False)
    image = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=False, blank=False)
    stock = models.IntegerField(default=0, null=False, blank=False)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name.title()


class ProductTags(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    product = models.ManyToManyField(Products, db_index=True, related_name="product_tags_mapping")

    def __str__(self):
        return self.name
    

class OrderDetails(models.Model):
    user = models.ForeignKey(CustomUser, null=False, blank=False, db_index=True, on_delete=models.CASCADE)
    order_hash = models.CharField(max_length=255, blank=False, null=False, db_index=True, editable = False, unique=True)
    order_date = models.DateTimeField(auto_now_add=True, db_index=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=False, blank=False)
    purchase_details = models.JSONField(blank=True, null=True)
    product_ids = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f'Order No :#{self.order_hash}'
    
        

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, null=False, blank=False, db_index=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_on']

class ProductCartMapper(models.Model):
    cart = models.ForeignKey(Cart, db_index=True, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, blank=False, db_index=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=False, blank=False)
