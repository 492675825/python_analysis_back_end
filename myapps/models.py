from django.db import models


# Create your models here.

class gold_data(models.Model):
    # 上海黄金交易所数据模型
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    item = models.CharField(max_length=100, null=True, blank=True, verbose_name="类别")
    open = models.CharField(max_length=100, null=True, blank=True, verbose_name="开盘价")
    high = models.CharField(max_length=100, null=True, blank=True, verbose_name="最高价")
    low = models.CharField(max_length=100, null=True, blank=True, verbose_name="最低价")
    close = models.CharField(max_length=100, null=True, blank=True, verbose_name="收盘价")
    up_or_down = models.CharField(max_length=100, null=True, blank=True, verbose_name="涨幅")
    version_date = models.BigIntegerField(null=False, blank=False, verbose_name="涨幅")

    class Meta:
        db_table = "temp_gold_data"
        verbose_name = "黄金价格"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item


class non_farm(models.Model):
    # 非农数据
    # version_date,current_value,predict_value,previous_value,refresh_date
    id = models.BigIntegerField(null=False, blank=False, primary_key=True, verbose_name="id")
    version_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="日期")
    current_value = models.CharField(max_length=20, null=True, blank=True, verbose_name="当前值")
    predict_value = models.CharField(max_length=20, null=True, blank=True, verbose_name="预测值")
    previous_value = models.CharField(max_length=20, null=True, blank=True, verbose_name="上一期值")
    refresh_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="更新时间")
    class Meta:
        db_table = 'tbl_non_farm_data'
        verbose_name = '非农数据'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.version_date
