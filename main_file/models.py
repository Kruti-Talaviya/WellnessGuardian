from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class Custom_User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'main_file'

    user_id = models.CharField(primary_key=True,max_length=10, unique=True,editable=False)
    USER_TYPES = (
        ('patient', 'Patient'),
        ('hospital', 'Hospital'), 
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField()
    username=models.CharField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username','user_type']

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_user_id()
        super(Custom_User, self).save(*args, **kwargs)


    def generate_user_id(self):
    
        from random import randint
        while True:
            new_user_id = 'MediU' + str(randint(100, 999))
            if not Custom_User.objects.filter(user_id=new_user_id).exists():
                return new_user_id

    def __str__(self):
        return self.user_id
    
    groups = models.ManyToManyField(Group, verbose_name='groups', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', related_name='custom_user_set', blank=True)


class login(models.Model):
    class Meta:
        app_label = 'main_file'
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)
    login_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.email} - {self.login_time}"

    def logout(self):
        self.logout_time = timezone.now()
        self.save()

class patientInfo(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    profile_photo = models.ImageField(upload_to='patient_photos/')
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.fullname
    
class hospitalInfo(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    address = models.CharField(max_length=199)
    # hospital_photo = models.ImageField(upload_to='hospital_photos/')
    contact_number = models.CharField(max_length=20)
    certificates = models.ImageField(upload_to='certificates/')
    speciality = models.CharField(max_length=200)

    def __str__(self):
        return self.hospital_name


    
class MediRecord(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE, related_name='medical_records')
    hospital_name = models.CharField(max_length=100)
    diseases = models.CharField(max_length=255)
    medi_document = models.FileField(upload_to='medi_documents/')
    note = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.hospital_name} - {self.diseases}"

