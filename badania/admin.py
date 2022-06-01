from django.contrib import admin
from .models import badania, morfologiaKrwi, probyWatrobowe

# Register your models here.
admin.site.register(badania)
admin.site.register(morfologiaKrwi)
admin.site.register(probyWatrobowe)