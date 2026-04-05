from django.contrib import admin
from .models import PoliticalParty, ElectoralList

# Register your models here.

admin.site.register(PoliticalParty)
admin.site.register(ElectoralList)