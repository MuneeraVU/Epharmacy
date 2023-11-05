# Create models for project.  models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
# Category model
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('med_by_cat', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


# Medicine model
class Medicine(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='medicines', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    stock = models.IntegerField(null=True)
    available = models.BooleanField(default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'medicine'
        verbose_name_plural = 'medicines'

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('medicine_details', args=[self.category.slug, self.slug])


# Prescription model
class Prescription(models.Model):
    patient_name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='prescriptions', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.patient_name)


# Model for cart
class CartItem(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.name} = {self.medicine.price}"


# Shipping address model
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=200)
    mobile = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.address)


