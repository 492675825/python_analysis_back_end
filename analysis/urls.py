from django.contrib import admin
from django.urls import path
import myapps.views as views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('admin/', admin.site.urls),
    path("gold/daily/data_etl/", views.gold_daily_data.as_view(), name="etl")
]
