from django.conf.urls import url

from exp_rest.api.v1 import views

urlpatterns = [
    url(r'^login/?$', views.login),
    url(r'^logout/?$', views.logout),
    url(r'^eps/(?P<token>[a-f0-9]+)/?$', views.get_eps),
    url(r'^eps/my/(?P<token>[a-f0-9]+)/?$', views.get_my_eps),
    url(r'^eps/(?P<id>[0-9]+)/(?P<token>[a-f0-9]+)/?$', views.get_ep),
    url(r'^opportunities/(?P<token>[a-f0-9]+)/?$', views.get_opportunities),
    url(r'^opportunities/(?P<id>[0-9]+)/(?P<token>[a-f0-9]+)/?$', views.get_opportunity),
]