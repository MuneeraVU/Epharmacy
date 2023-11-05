from django.contrib import admin
from .models import Category, Medicine


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


# Register models Category,Medicine
admin.site.register(Category, CategoryAdmin)
admin.site.register(Medicine)
