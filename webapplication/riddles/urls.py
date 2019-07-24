from django.conf.urls import url
from .views import polls_list, polls_detail,lastdata_view,lastdata_view_aver_1min
from django.urls import path

from . import views

app_name = 'riddles'

urlpatterns = [
    url(r'^$', views.present, name='present'),
    url(r'^present/', views.present, name='present'),
    url(r'^history/', views.history, name='history'),
    url(r'^journal/', views.journal, name='journal'),
    url(r'^configure/', views.configure, name='configure'),
    path("polls/", polls_list, name="polls_list"),
    path("polls/<int:pk>/", polls_detail, name="polls_detail"),
    path("api/lastdata/<int:sec>/", lastdata_view, name="lastdata_view"),
    path("api/lastdata1min/<int:minute>/", lastdata_view_aver_1min, name="lastdata_view_aver_1min")

    
 ]