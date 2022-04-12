# Generated by Django 4.0.3 on 2022-04-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0006_cctv_china_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='cctv_economy_news',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('version_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='新闻日期')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='标题')),
                ('brief', models.CharField(blank=True, max_length=1000, null=True, verbose_name='概要')),
                ('keyword', models.CharField(blank=True, max_length=1000, null=True, verbose_name='关键词')),
                ('url', models.CharField(blank=True, max_length=1000, null=True, verbose_name='网页连接')),
                ('refresh_date', models.CharField(blank=True, max_length=100, null=True, verbose_name='入库时间')),
            ],
            options={
                'verbose_name': '央视经济新闻',
                'verbose_name_plural': '央视经济新闻',
                'db_table': 'tbl_d_news_cctv_economy',
            },
        ),
        migrations.AlterModelOptions(
            name='cctv_china_news',
            options={'verbose_name': '央视国内新闻', 'verbose_name_plural': '央视国内新闻'},
        ),
    ]