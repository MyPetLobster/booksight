from django.contrib import admin
from .models import Spine, Book, Scan

# Register your models here.
admin.site.register(Spine)
admin.site.register(Book)
admin.site.register(Scan)