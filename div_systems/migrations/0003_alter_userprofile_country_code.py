# Generated by Django 4.0.5 on 2022-07-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('div_systems', '0002_userprofile_is_active_userprofile_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country_code',
            field=models.CharField(max_length=20),
        ),
    ]