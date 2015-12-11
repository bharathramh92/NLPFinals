from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.index_view, name="index"),
    url(r'^(?P<product_id>[0-9a-zA-Z]+)/$', views.product_view, name='product'),

]