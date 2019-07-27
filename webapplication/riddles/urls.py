from django.conf.urls import url
from .views import polls_list, polls_detail,lastdata_view,lastdata_view_aver_1min,lastdata_view_1day
from .views import lastdata_view_1month,lastdata_view_aver_1min_from_time,lastdata_view_from_1day,get_journal,get_alarm

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
    path("api/lastdata1min/<int:minute>/", lastdata_view_aver_1min, name="lastdata_view_aver_1min"),
    path("api/lastdata_view_1day/", lastdata_view_1day, name="lastdata_view_1day"),
    path("api/lastdata_view_1month/", lastdata_view_1month, name="lastdata_view_1month"),
    path("api/aver1minfrom/<int:minute>/<str:t_date>", lastdata_view_aver_1min_from_time, name="lastdata_view_aver_1min_from_time"),
    path("api/aver1dayfrom/<str:t_date>", lastdata_view_from_1day, name="lastdata_view_from_1day"),
    path("api/get_journal/", get_journal, name="get_journal"),
    path("api/get_alarm/", get_alarm, name="get_alarm")



 ]