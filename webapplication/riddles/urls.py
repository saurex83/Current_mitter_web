from django.conf.urls import url

from . import views

app_name = 'riddles'

urlpatterns = [
    url(r'^$', views.present, name='present'),
    url(r'^present/', views.present, name='present'),
    url(r'^history/', views.history, name='history'),
    url(r'^journal/', views.journal, name='journal'),
    url(r'^configure/', views.configure, name='configure')
 ]