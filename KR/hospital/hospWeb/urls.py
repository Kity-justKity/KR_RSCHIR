from django.urls import path, re_path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^appointment/new/$', views.make_appointment, name='make-appointment'),
    re_path(r'^my_appointments/$', views.AppointmentsUserListView.as_view(), name='my-appointments'),
    re_path(r'^appointments/$', views.AppointmentsListView.as_view(), name='appointments'),
    re_path(r'^appointment/(?P<pk>\d+)$', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    re_path(r'^appointment/(?P<pk>\d+)/update_user/$', views.AppointmentUserUpdate.as_view(), name='appointment-update-user'),
    re_path(r'^appointment/(?P<pk>\d+)/update/$', views.AppointmentUpdate.as_view(), name='appointment-update'),
    re_path(r'^appointment/(?P<pk>\d+)/delete/$', views.AppointmentDelete.as_view(), name='appointment-delete'),
    re_path(r'^register/$', views.register, name='register'),
]

urlpatterns += [
    path('doctors/', views.DoctorListView.as_view(), name='doctors'),
    re_path(r'^doctor/(?P<pk>\d+)$', views.DoctorDetailView.as_view(), name='doctor-detail'),
    re_path(r'^doctor/create/$', views.DoctorCreate.as_view(), name='doctor-create'),
    re_path(r'^doctor/(?P<pk>\d+)/update/$', views.DoctorUpdate.as_view(), name='doctor-update'),
    re_path(r'^doctor/(?P<pk>\d+)/delete/$', views.DoctorDelete.as_view(), name='doctor-delete'),
]

urlpatterns += [
    path('specialities/', views.SpecialityListView.as_view(), name='specialities'),
    re_path(r'^speciality/(?P<pk>\d+)$', views.SpecialityDetailView.as_view(), name='speciality-detail'),
    re_path(r'^speciality/create/$', views.SpecialityCreate.as_view(), name='speciality-create'),
    re_path(r'^speciality/(?P<pk>\d+)/update/$', views.SpecialityUpdate.as_view(), name='speciality-update'),
    re_path(r'^speciality/(?P<pk>\d+)/delete/$', views.SpecialityDelete.as_view(), name='speciality-delete'),
]

urlpatterns += [
    path('doctor_speciality_list/', views.DoctorSpecialityListView.as_view(), name='doctor-speciality-list'),
    re_path(r'^doctor_speciality/(?P<pk>\d+)$', views.DoctorSpecialityDetailView.as_view(), name='doctor-speciality-detail'),
    re_path(r'^doctor_speciality/create/$', views.DoctorSpecialityCreate.as_view(), name='speciality-create'),
    re_path(r'^doctor_speciality/(?P<pk>\d+)/update/$', views.DoctorSpecialityUpdate.as_view(), name='speciality-update'),
    re_path(r'^doctor_speciality/(?P<pk>\d+)/delete/$', views.DoctorSpecialityDelete.as_view(), name='speciality-delete'),
]