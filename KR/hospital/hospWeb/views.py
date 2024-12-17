from django.shortcuts import render
from django.views import generic
from .models import Doctor, Speciality, DoctorSpeciality, Service, DoctorSpecialityService, Schedule, Appointment
from django.contrib.auth.decorators import login_required
from .forms import NewAppointmentForm, UserRegisterForm, AppointmentUserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User


def index(request):
    head_med = Doctor.objects.all().count()

    return render(
        request,
        'index.html',
        context={'head_med': head_med},
    )


class DoctorListView(generic.ListView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        doc_spec_list = []
        for doctor in context['doctor_list']:
            doc_spec = DoctorSpeciality.objects.filter(doctor__id__exact=doctor.id)
            # doctor.doctorspeciality_set.all() то же самое
            specialties = []
            for spec in doc_spec:
                specialties.append(spec.speciality.name)
            #     specialties.append(s.speciality)
            doc_spec_list.append(specialties)
            # context['doc_spec'][str(doctor)] = specialties

        context['zip_doc_spec'] = zip(context['doctor_list'], doc_spec_list)
        return context


class DoctorDetailView(generic.DetailView):
    model = Doctor


@login_required
def make_appointment(request):
    if request.method == 'POST':
        doc_spec_id = request.GET['doc_spec_id']
        form = NewAppointmentForm(doc_spec_id, request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            date.available = 'u'
            date.save()
            service = form.cleaned_data['service']
            # doc_spec_serv = service.doctorspecialityservice_set.all().filter(doctorspeciality__id__exact=doc_spec_id)
            patient = request.user
            new_appointment = Appointment(patient=patient, doc_spec_serv=service, date=date)
            new_appointment.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        doc_spec_id = request.GET['doc_spec_id']
        form = NewAppointmentForm(doc_spec_id)

    return render(request, 'hospWeb/make_appointment.html', {'form': form, '???doc_spec_id': doc_spec_id})

# def appointment_user_change(request):
#     if request.method == 'POST':
#         form = AppointmentUserChangeForm(request.POST)
#
#         if form.is_valid():
#             date = form.cleaned_data['date']
#             date.available = 'u'
#             date.save()
#             patient = request.user
#             new_appointment = Appointment(patient=patient, doc_spec_serv=service, date=date)
#             new_appointment.save()
#             return HttpResponseRedirect(reverse('index'))
#
#     else:
#         doc_spec_id = request.GET['doc_spec_id']
#         form = NewAppointmentForm(doc_spec_id)
#
#     return render(request, 'hospWeb/make_appointment.html', {'form': form, '???doc_spec_id': doc_spec_id})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserRegisterForm()
    return render(request, 'hospWeb/register.html', {'form': form})


class AppointmentsUserListView(PermissionRequiredMixin, generic.ListView):
    model = Appointment
    permission_required = 'hospWeb.view_appointments_visitor'
    template_name = 'hospWeb/appointment_list_user.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).filter(relevance__exact='a').order_by('date')

    def get_context_data(self, **kwargs):
        context = super(AppointmentsUserListView, self).get_context_data(**kwargs)
        past_appointment_list = Appointment.objects.filter(patient=self.request.user).filter(
            relevance__exact='p').order_by('date')
        context['past_appointment_list'] = past_appointment_list
        return context


class AppointmentsListView(PermissionRequiredMixin, generic.ListView):
    model = Appointment
    permission_required = 'hospWeb.view_appointments'

    def get_queryset(self):
        return Appointment.objects.filter(relevance__exact='a').order_by('date')

    def get_context_data(self, **kwargs):
        context = super(AppointmentsListView, self).get_context_data(**kwargs)
        past_appointment_list = Appointment.objects.filter(relevance__exact='p').order_by('date')
        context['past_appointment_list'] = past_appointment_list
        return context


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment


class AppointmentUserUpdate(PermissionRequiredMixin, UpdateView):
    model = Appointment
    fields = ['date']
    permission_required = 'hospWeb.change_appointment_visitor'
    # template_name = 'hospWeb/appointment_list_user.html'


class AppointmentUpdate(PermissionRequiredMixin, UpdateView):
    model = Appointment
    fields = '__all__'
    permission_required = 'hospWeb.change_appointment'


class AppointmentDelete(PermissionRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointments')
    permission_required = 'hospWeb.delete_appointment'



class DoctorCreate(PermissionRequiredMixin, CreateView):
    model = Doctor
    fields = '__all__'
    permission_required = 'hospWeb.add_doctor'


class DoctorUpdate(PermissionRequiredMixin, UpdateView):
    model = Doctor
    fields = '__all__'
    permission_required = 'hospWeb.change_doctor'


class DoctorDelete(PermissionRequiredMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctors')
    permission_required = 'hospWeb.delete_doctor'



class SpecialityListView(generic.ListView):
    model = Speciality


class SpecialityDetailView(generic.DetailView):
    model = Speciality


class SpecialityCreate(PermissionRequiredMixin, CreateView):
    model = Speciality
    fields = '__all__'
    permission_required = 'hospWeb.add_speciality'


class SpecialityUpdate(PermissionRequiredMixin, UpdateView):
    model = Speciality
    fields = '__all__'
    permission_required = 'hospWeb.change_speciality'


class SpecialityDelete(PermissionRequiredMixin, DeleteView):
    model = Speciality
    success_url = reverse_lazy('specialities')
    permission_required = 'hospWeb.delete_speciality'



class DoctorSpecialityListView(generic.ListView):
    model = DoctorSpeciality


class DoctorSpecialityDetailView(generic.DetailView):
    model = DoctorSpeciality


class DoctorSpecialityCreate(PermissionRequiredMixin, CreateView):
    model = DoctorSpeciality
    fields = '__all__'
    permission_required = 'hospWeb.add_doctorspeciality'


class DoctorSpecialityUpdate(PermissionRequiredMixin, UpdateView):
    model = DoctorSpeciality
    fields = '__all__'
    permission_required = 'hospWeb.change_doctorspeciality'


class DoctorSpecialityDelete(PermissionRequiredMixin, DeleteView):
    model = DoctorSpeciality
    success_url = reverse_lazy('doctor-speciality-list')
    permission_required = 'hospWeb.delete_doctorspeciality'
