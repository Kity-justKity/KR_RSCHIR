from django.contrib import admin
from .models import Doctor, Speciality, DoctorSpeciality, Service, DoctorSpecialityService, Schedule, Appointment, Review

admin.site.register(Doctor)
admin.site.register(Speciality)
admin.site.register(DoctorSpeciality)
admin.site.register(Service)
admin.site.register(DoctorSpecialityService)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(Review)
