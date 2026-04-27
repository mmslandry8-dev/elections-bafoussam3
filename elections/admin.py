from django.contrib import admin
from .models import (
    Election,
    Commune,
    Center,
    PollingStation,
    Party,
    ElectoralList,
    Vote,
    PhysicalResult
)

admin.site.register(Election)
admin.site.register(Commune)
admin.site.register(Center)
admin.site.register(PollingStation)
admin.site.register(Party)
admin.site.register(ElectoralList)
admin.site.register(Vote)
admin.site.register(PhysicalResult)