# Generated by Django 4.0.3 on 2022-04-09 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gold_data',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('item', models.CharField(blank=True, max_length=100, null=True, verbose_name='类别')),
                ('open', models.CharField(blank=True, max_length=100, null=True, verbose_name='开盘价')),
                ('high', models.CharField(blank=True, max_length=100, null=True, verbose_name='最高价')),
                ('low', models.CharField(blank=True, max_length=100, null=True, verbose_name='最低价')),
                ('close', models.CharField(blank=True, max_length=100, null=True, verbose_name='收盘价')),
                ('up_or_down', models.CharField(blank=True, max_length=100, null=True, verbose_name='涨幅')),
                ('version_date', models.BigIntegerField(verbose_name='涨幅')),
            ],
            options={
                'verbose_name': '黄金价格',
                'verbose_name_plural': '黄金价格',
                'db_table': 'temp_gold_data',
            },
        ),
    ]
