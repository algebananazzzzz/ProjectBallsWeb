# Generated by Django 3.1.4 on 2021-05-01 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_boardmodel_uploaddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippetmodel',
            name='Speed',
            field=models.IntegerField(default=1),
        ),
    ]