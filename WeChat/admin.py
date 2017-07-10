from django.contrib import admin

# Register your models here.
from .models import feedback
class show_list(admin.ModelAdmin):
    list_display = ('fk_content','user','time',)
admin.site.register(feedback,show_list)