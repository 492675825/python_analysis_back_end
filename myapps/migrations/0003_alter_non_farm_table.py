# Generated by Django 4.0.3 on 2022-04-10 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0002_non_farm'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='non_farm',
            table='tbl_non_farm_data',
        ),
    ]