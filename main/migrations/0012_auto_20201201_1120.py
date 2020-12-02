# Generated by Django 3.1.3 on 2020-12-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_boardmodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cancel_recording_key',
            field=models.IntegerField(default=99),
        ),
        migrations.AddField(
            model_name='user',
            name='end_recording_key',
            field=models.IntegerField(default=32),
        ),
        migrations.AddField(
            model_name='user',
            name='start_recording_key',
            field=models.IntegerField(default=115),
        ),
        migrations.AddField(
            model_name='user',
            name='useSelect',
            field=models.BooleanField(default=True),
        ),
    ]
