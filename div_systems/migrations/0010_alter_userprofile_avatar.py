# Generated by Django 4.0.5 on 2022-07-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('div_systems', '0009_alter_userprofile_avatar_alter_userprofile_birthdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(default='s.jpg', upload_to='avatars'),
            preserve_default=False,
        ),
    ]
