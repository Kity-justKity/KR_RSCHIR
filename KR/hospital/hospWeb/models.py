from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Doctor(models.Model):
    last_name = models.CharField(max_length=20, help_text='Введите фамилию врача')
    first_name = models.CharField(max_length=20, help_text='Введите имя врача')
    patronymic = models.CharField(max_length=20, help_text='Введите отчество врача')
    education = models.TextField(max_length=1000, help_text='Введите образование врача')
    experience = models.TextField(max_length=1000, help_text='Введите опыт работы врача')

    def __str__(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.patronymic

    def get_absolute_url(self):
        return reverse('doctor-detail', args=[str(self.id)])


class Speciality(models.Model):
    name = models.CharField(max_length=30, help_text='Введите название специальности')
    description = models.CharField(max_length=200, help_text='Введите описание специальности')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('speciality-detail', args=[str(self.id)])


class DoctorSpeciality(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)

    # speciality_name = speciality.description

    def __str__(self):
        return self.doctor.last_name + '_' + self.speciality.name

    def get_absolute_url(self):
        return reverse('doctorspeciality-detail', args=[str(self.id)])


class Service(models.Model):
    name = models.CharField(max_length=100, help_text='Введите название услуги')
    description = models.CharField(max_length=200, help_text='Введите описание услуги')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(help_text='Введите стоимость услуги')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-detail', args=[str(self.id)])


class DoctorSpecialityService(models.Model):
    doctorSpeciality = models.ForeignKey(DoctorSpeciality, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    ACCESS_TYPE = (
        ('u', 'User'),
        ('s', 'Staff'),
    )
    access = models.CharField(max_length=1, choices=ACCESS_TYPE, default='u', help_text='Кто может создать запись')

    # class Meta:
    #     permissions = (("some_permission", "Some permission yeah"),)

    def __str__(self):
        return self.service.name + '_' + str(self.doctorSpeciality)

    def get_absolute_url(self):
        return reverse('doctorspecialityservice-detail', args=[str(self.id)])


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text='Введите дату и время свободные для записи')
    AVAILABLE_STATUS = (
        ('a', 'Available'),
        ('u', 'Unavailable'),
    )
    available = models.CharField(max_length=1, choices=AVAILABLE_STATUS, default='a', help_text='Доступна ли дата для записи')

    def __str__(self):
        return str(self.doctor) + '_' + str(self.date)

    def get_absolute_url(self):
        return reverse('schedule-detail', args=[str(self.id)])


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_spec_serv = models.ForeignKey(DoctorSpecialityService, on_delete=models.CASCADE)

    RELEVANCE_STATUS = (
        ('a', 'Actual'),
        ('p', 'Past'),
    )
    relevance = models.CharField(max_length=1, choices=RELEVANCE_STATUS, default='a', help_text='Актуальность записи')

    date = models.OneToOneField(Schedule, on_delete=models.DO_NOTHING)
    # limit_choices_to = {'available': 'a'}

    class Meta:
        permissions = (("create_appointment_visitor", "Visitor can create appointment"),
                       ("change_appointment_visitor", "Visitor can change appointment"),
                       ("view_appointments_visitor", "Visitor can view appointments"),
                       ("view_appointments", "Staff can view appointments"),)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('appointment-detail', args=[str(self.id)])


class Review(models.Model):
    patient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, help_text='Введите комментарий')

    MARKS = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
        ('4', 'Four'),
        ('5', 'Five'),
    )
    mark = models.CharField(max_length=1, choices=MARKS, default='5', help_text='Оценка врача')

    def __str__(self):
        return str(self.doctor) + '_' + str(self.mark)

    # def get_absolute_url(self):
    #     return reverse('review-detail', args=[str(self.id)])
