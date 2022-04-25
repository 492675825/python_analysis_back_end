from celery import Celery
from mycelery import config
from datetime import timedelta

# 创建celery主程序
app = Celery()

# 加载配置
app.config_from_object("mycelery.config")
# 加载配置
app.autodiscover_tasks(["mycelery.news"])

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'get_news': {
            'task': 'mycelery.news.tasks.get_news',
            'schedule': timedelta(seconds=60),
            'args': ()
        }
    }
)
