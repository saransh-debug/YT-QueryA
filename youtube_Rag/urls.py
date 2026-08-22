
from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.test),
    path("details/",views.Db_details)
]
