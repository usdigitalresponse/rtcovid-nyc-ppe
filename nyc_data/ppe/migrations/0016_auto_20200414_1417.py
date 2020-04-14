# Generated by Django 3.0.5 on 2020-04-14 14:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ppe', '0015_purchase_received_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataimport',
            name='data_file',
            field=models.TextField(choices=[('PPE_ORDERINGCHARTS_DATE_XLSX', 'PPE_ORDERINGCHARTS_DATE_XLSX'), ('SUPPLIERS_PARTNERS_XLSX', 'SUPPLIERS_PARTNERS_XLSX'), ('INVENTORY', 'INVENTORY'), ('FACILITY_DELIVERIES', 'FACILITY_DELIVERIES'), ('HOSPITAL_DEMANDS', 'HOSPITAL_DEMANDS')], default=None),
        ),
        migrations.CreateModel(
            name='WeeklyDemand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.TextField()),
                ('demand', models.IntegerField()),
                ('week_start_date', models.DateField()),
                ('week_end_date', models.DateField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ppe.DataImport')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
