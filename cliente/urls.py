from django.conf.urls import patterns, url

from cliente import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    ## goto new user
    url(r'^newuser/$', views.newuser, name='newuser'),

    url(r'^login/$', views.login, name='login'),

    url(r'^receta/$', views.receta, name='receta'),

    url(r'^cerrar/$', views.cerrar, name='cerrar'),

)


