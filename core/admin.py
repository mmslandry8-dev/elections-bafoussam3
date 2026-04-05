from django.contrib import admin
from .models import Commune, CentreVote, BureauVote
# Register your models here.

admin.site.register(Commune)
admin.site.register(CentreVote)
admin.site.register(BureauVote)