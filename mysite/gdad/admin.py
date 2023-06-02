from django.contrib import admin

# Register your models here.

from .models import G4, GeneSequence, Gda

admin.site.register(G4)
admin.site.register(GeneSequence)
admin.site.register(Gda)
