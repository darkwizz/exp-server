from django.conf.urls import url

from exp_rest.api.v1 import views

urlpatterns = [
    url(r'^login/?$', views.login),
    url(r'^logout/?$', views.logout),
    url(r'^eps/?$', views.get_eps),
    url(r'^eps/my/?$', views.get_my_eps),
    url(r'^eps/(?P<id>[0-9]+)/?$', views.get_ep),
    url(r'^opportunities/?$', views.get_opportunities),
    url(r'^opportunities/(?P<id>[0-9]+)/?$', views.get_opportunity),
]