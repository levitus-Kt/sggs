from django.contrib import admin
from .models import LessonQuantity, Holidays, UploadFile

admin.site.register(LessonQuantity)
admin.site.register(Holidays)
admin.site.register(UploadFile)