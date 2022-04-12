from django.contrib import admin
from django.urls import path
import myapps.views as views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('admin/', admin.site.urls),
    path("gold/daily/data_etl/", views.gold_daily_data.as_view(), name="etl"),
    path("nonfarm/data/full/", views.non_farm_data.as_view(), name="nonfarm_full"),
    path("nonfarm/data/delta/", views.nonfarm_data_delta.as_view(), name="nonfarm_delta"),
    path("news/cctv/news/", views.cctv_world_news.as_view(), name="cctv_news")
]

