from django.contrib import admin
from .models import Lekarz, LekarzProfil, Pacjent, PacjentProfil, Diagnosta, DiagnostaProfil

# Register your models here.
admin.site.register(Lekarz)
admin.site.register(LekarzProfil)
admin.site.register(Pacjent)
admin.site.register(PacjentProfil)
admin.site.register(Diagnosta)
admin.site.register(DiagnostaProfil)