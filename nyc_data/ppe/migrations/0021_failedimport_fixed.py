# Generated by Django 3.0.5 on 2020-04-19 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppe', '0020_failedimport'),
    ]

    operations = [
        migrations.AddField(
            model_name='failedimport',
            name='fixed',
            field=models.BooleanField(default=False),
        ),
    ]
