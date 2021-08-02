from django.contrib import admin
from .models import Institution


# Register your models here.

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
