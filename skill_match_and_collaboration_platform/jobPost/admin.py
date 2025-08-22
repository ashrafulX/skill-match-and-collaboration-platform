from django.contrib import admin

# Register your models here.
from .models import JobPost,Application,Notification

admin.site.register(JobPost)
admin.site.register(Application)
admin.site.register(Notification)
