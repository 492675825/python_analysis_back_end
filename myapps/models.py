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


class cctv_world_news(models.Model):
    # version_date,title,brief,keyword,url
    id = models.BigAutoField(null=False, blank=False, primary_key=True, verbose_name="编号", )
    version_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="新闻日期")
    title = models.CharField(max_length=1000, null=True, blank=True, verbose_name="标题")
    brief = models.CharField(max_length=1000, null=True, blank=True, verbose_name="概要")
    keyword = models.CharField(max_length=1000, null=True, blank=True, verbose_name="关键词")
    url = models.CharField(max_length=1000, null=True, blank=True, verbose_name="网页连接")
    refresh_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="入库时间")
    news_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="新闻类别")

    class Meta:
        db_table = 'tbl_d_news_cctv_world'
        verbose_name = '央视国际新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.title

class cctv_china_news(models.Model):
    # version_date,title,brief,keyword,url
    id = models.BigAutoField(null=False, blank=False, primary_key=True, verbose_name="编号", )
    version_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="新闻日期")
    title = models.CharField(max_length=1000, null=True, blank=True, verbose_name="标题")
    brief = models.CharField(max_length=1000, null=True, blank=True, verbose_name="概要")
    keyword = models.CharField(max_length=1000, null=True, blank=True, verbose_name="关键词")
    url = models.CharField(max_length=1000, null=True, blank=True, verbose_name="网页连接")
    refresh_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="入库时间")
    news_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="新闻类别")

    class Meta:
        db_table = 'tbl_d_news_cctv_china'
        verbose_name = '央视国内新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.title

class cctv_economy_news(models.Model):
    # version_date,title,brief,keyword,url
    id = models.BigAutoField(null=False, blank=False, primary_key=True, verbose_name="编号", )
    version_date = models.CharField(max_length=50, null=True, blank=True, verbose_name="新闻日期")
    title = models.CharField(max_length=1000, null=True, blank=True, verbose_name="标题")
    brief = models.CharField(max_length=1000, null=True, blank=True, verbose_name="概要")
    keyword = models.CharField(max_length=1000, null=True, blank=True, verbose_name="关键词")
    url = models.CharField(max_length=1000, null=True, blank=True, verbose_name="网页连接")
    refresh_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="入库时间")
    news_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="新闻类别")

    class Meta:
        db_table = 'tbl_d_news_cctv_economy'
        verbose_name = '央视经济新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.title


