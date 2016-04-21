from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stream', views.stream, name='stream'),
    url(r'^search', views.search, name='search'),
    url(r'^fresh', views.fresh, name='fresh'),
]
