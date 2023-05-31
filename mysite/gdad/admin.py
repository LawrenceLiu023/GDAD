from django.contrib import admin

# Register your models here.

from .models import G4, GeneSequence, Tfbs, Gda

admin.site.register(G4)
admin.site.register(GeneSequence)
admin.site.register(Tfbs)
admin.site.register(Gda)
