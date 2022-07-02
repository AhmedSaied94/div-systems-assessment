# Generated by Django 4.0.5 on 2022-07-02 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('div_systems', '0005_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(blank=True, default='1995-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country_code',
            field=models.CharField(blank=True, default='EG', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, default='ahmed', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, default='male', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, default='said', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='1158626091', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
