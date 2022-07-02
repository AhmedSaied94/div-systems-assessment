from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserProfileManager(BaseUserManager):

    def create_user(self, first_name, last_name, country_code, phone_number, gender, birthdate, password=None, **kwargs):
        if not phone_number:
            raise ValueError('You must enter a phone number')

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

    first_name = models.CharField(max_length=50, )
    last_name = models.CharField(max_length=50, )
    country_code = models.CharField(max_length=20, )
    phone_number = models.CharField(
        max_length=20, unique=True, )
    gender = models.CharField(
        max_length=20, )
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, )
    avatar = models.FileField(upload_to='avatars')
    email = models.CharField(
        max_length=254, null=True, blank=True, unique=True)
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
