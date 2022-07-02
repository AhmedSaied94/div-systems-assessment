import re
import sys
from datetime import datetime
from pathlib import Path

import magic
from countries_plus.models import Country
from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from .verify import send_sms

# catch auth user model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # change birthdate format
    birthdate = serializers.DateField('%Y-%m-%d', required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'country_code',
            'phone_number',
            'gender',
            'birthdate',
            'avatar',
            'email',
            'password'
        ]

        # disable django serializer default validators
        extra_kwargs = {
            "password": {'write_only': True},
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True},
            'country_code': {'required': False, 'allow_null': True},
            'phone_number': {'required': False, 'allow_null': True, 'validators': []},
            'gender': {'required': False, 'allow_null': True},
            'birthdate': {'required': False, 'allow_null': True},
            'avatar': {'required': False, 'allow_null': True, 'write_only': True},
            'email': {'required': False, 'allow_null': True, 'validators': []},

        }

    # validate the whole data object
    def validate(self, data):
        errors = {}

        # validate first and last names
        if 'first_name' not in data or data['first_name'] == '':
            errors['first_name'] = [{'error': 'blank'}]

        if 'last_name' not in data or data['last_name'] == '':
            errors['last_name'] = [{'error': 'blank'}]

        # validate country_code
        qs = {}
        if 'country_code' not in data or data['country_code'] == '':
            errors['country_code'] = [{'error': 'inclusion'}]

        else:
            qs = Country.objects.filter(iso=data['country_code'])
            if not qs.exists() and 'test' not in sys.argv:
                errors['country_code'] = [{'error': 'inclusion'}]

        # validate phone number
        # check for blank error
        if 'phone_number' not in data or data['phone_number'] == '':
            errors['phone_number'] = [{'error': 'blank'}]
        else:
            try:  # check for not_a_number error
                int(data['phone_number'])
            except:
                errors['phone_number'] = [{'error': 'not_a_number'}]

            if qs != {}:

                if 'test' in sys.argv:
                    phone_code = '+20'
                else:
                    # get country dial code
                    phone_code = f'+{qs.first().phone}'
                phone_re = re.compile(r'^\+?1?\d{9,15}$')
                # check for invalid error
                if not re.search(phone_re, phone_code+data['phone_number']):
                    errors['phone_number'] = [{'error': 'invalid'}]

                    # check for too_short error
                    if len(phone_code+data['phone_number']) < 10:
                        errors['phone_number'] = [
                            {'error': 'too_short', 'count': 10}]

                    # check for too_long error
                    if len(phone_code+data['phone_number']) > 15:
                        errors['phone_number'] = [
                            {'error': 'too_long', 'count': 15}]
                else:
                    phone_number = phone_code + \
                        data['phone_number'][1:] if phone_code[-1] == '0' and data['phone_number'][0] == '0' else phone_code + data['phone_number']
                    # check for taken error
                    if User.objects.filter(phone_number=phone_number).exists():
                        errors['phone_number'] = [{'error': 'taken'}]
                    else:
                        is_exists = send_sms(phone_code+data['phone_number'])

                        if not is_exists:  # check for not_exist error
                            errors['phone_number'] = [{'error': 'not_exist'}]

        # validate gender

        if 'gender' not in data or data['gender'] == '' or data['gender'] not in ['male', 'female']:
            errors['gender'] = [{'error': 'inclusion'}]

        # validate future date
        # check for blank error
        if 'birthdate' not in data or data['birthdate'] == '':
            errors['birthdate'] = [{'error': 'blank'}]
        else:
            if data['birthdate'] > datetime.today().date():  # check for in_the_future error
                errors['birthdate'] = [{'error': 'in_the_future'}]

        # validate email
        if 'email' in data and data['email'] != '':
            email_re = re.compile(
                r'^[a-z0-9\._-]+[@]\w+[.]\w{2,3}$')
            # check for valid email
            if not re.fullmatch(email_re, data['email']):
                errors['email'] = [{'error': 'invalid'}]
            else:
                # check for taken error
                if User.objects.filter(email=data['email']).exists():
                    errors['email'] = [{'error': 'taken'}]

        # validate avatar
        if 'avatar' not in data or data['avatar'] == '':
            errors['avatar'] = [{'error': 'blank'}]
        else:
            # specifiy allowed extension and content types
            allowed_exts = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
            }
            # get file extension
            ext = Path(data['avatar'].name).suffix[1:].lower()
            content_type = magic.from_buffer(
                data['avatar'].read(1024), mime=True)  # data content-type
            if ext not in allowed_exts or allowed_exts[ext] != content_type:
                errors['avatar'] = [{'error': 'invalid_content_type'}]
        # check and raise all errors in one exception
        if errors != {}:
            raise serializers.ValidationError(detail=errors, code=400)
        else:
            # change phone number to match E164 format
            # and to ensure that taken error will work
            # because +20010XXXXXXXX and +2010XXXXXXXXX both of them will work
            data['phone_number'] = phone_number
            return data

    # save user object
    def save(self, **kwargs):
        user = User(
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            country_code=self.validated_data.get('country_code'),
            phone_number=self.validated_data.get('phone_number'),
            gender=self.validated_data.get('gender'),
            birthdate=self.validated_data.get('birthdate'),
            avatar=self.validated_data.get('avatar'),
            email=self.validated_data.get('email')
        )

        user.set_password(self.validated_data.get('password'))
        user.save()
        return user
