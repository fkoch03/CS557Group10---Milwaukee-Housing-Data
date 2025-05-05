from django.contrib import admin
from .models import *

import MilwaukeeProperties

# Register your models here.

admin.site.register(Alderman)
admin.site.register(Property)
admin.site.register(Favorite)
admin.site.register(CondoProject)
admin.site.register(Comment)
admin.site.register(Sale)
admin.site.register(Realtor)
admin.site.register(RealtorCompany)
admin.site.register(District)
admin.site.register(Location)


