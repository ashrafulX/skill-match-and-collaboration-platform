from django.contrib import admin

# Register your models here.
from .models import Categories

class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display=['name','slug']

admin.site.register(Categories,CategoriesAdmin)