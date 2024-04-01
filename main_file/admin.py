from django.contrib import admin
from .models import login , hospitalInfo, patientInfo,MediRecord,Custom_User
# Register your models here.

admin.site.register(Custom_User)
admin.site.register(hospitalInfo)
admin.site.register(login)
admin.site.register(patientInfo)
admin.site.register(MediRecord)