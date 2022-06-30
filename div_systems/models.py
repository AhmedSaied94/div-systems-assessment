from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.apps import apps
from django.contrib.auth.validators import UnicodeUsernameValidator
from countries_plus.models import Country
from django.urls import reverse
from django.core.validators import RegexValidator
# Create your models here.


class UserProfileManager(BaseUserManager):

    def create_user(self, first_name, last_name, country_code, phone_number, gender, birthdate, password=None, **kwargs):
        if not phone_number:
            raise ValueError('You must enter an email address')
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name)
        # first_name = GlobalUserModel.normalize_first_name(first_name)
        # last_name = GlobalUserModel.normalize_last_name(last_name)
        # country_code = GlobalUserModel.normalize_country_code(country_code)
        # phone_number = GlobalUserModel.normalize_phone_number(phone_number)
        # gender = GlobalUserModel.normalize_gender(gender)

        user = self.model(first_name=first_name, last_name=last_name,
                          country_code=country_code, phone_number=phone_number, gender=gender, birthdate=birthdate, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, country_code, phone_number, gender, birthdate, password, **kwargs):
        user = self.create_user(
            first_name, last_name, country_code, phone_number, gender, birthdate, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        male = 'male', 'MALE'
        female = 'female', 'FEMALE'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'country_code', 'gender', 'birthdate']

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})
