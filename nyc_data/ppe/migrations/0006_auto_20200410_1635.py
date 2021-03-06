# Generated by Django 3.0.5 on 2020-04-10 16:35

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


def truncate_tables(apps, schema_editor):
    Inventory = apps.get_model("ppe", "Inventory")
    Delivery = apps.get_model("ppe", "Delivery")
    Purchase = apps.get_model("ppe", "Purchase")
    Inventory.objects.all().delete()
    Delivery.objects.all().delete()
    Purchase.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("ppe", "0005_auto_20200410_1635"),
    ]

    operations = [migrations.RunPython(truncate_tables)]
