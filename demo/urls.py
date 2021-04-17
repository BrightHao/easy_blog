from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^about/$', views.about),
    url(r'^article/$', views._Article.as_view()),
    url(r'^article/(?P<id>\d+)', views.article_detail),
    url(r'^article_detail/$', views.article_detail),
    url(r'^mood/$', views._Mood.as_view()),
    url(r'^search/$', views.Search.as_view()),
    url(r'^class/(?P<id>\d+)', views.Class),
    url(r'^tag/(?P<id>\d+)', views.tag),
]

