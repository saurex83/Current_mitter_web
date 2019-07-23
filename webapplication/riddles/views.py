from django.http import HttpResponse
from django.template import Context, loader
from django import template
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import datetime
from .models import Curdata

def present(request):
	#template = loader.get_template("index.html")
	template = loader.get_template("present.html")
	#context = template.Context({'name': 'Adrian'})
	#t = template.Template('My name is {{ name }}.')
	#c = template.Context({'name': 'Adrian'})

	return HttpResponse(template.render({"phase1":True ,"phase2":False, "phase3":False}))
    #return HttpResponse("Hello, World!")


def history(request):
	template = loader.get_template("history.html")
	return HttpResponse(template.render())
	#return HttpResponse(template.render()


def journal(request):
	template = loader.get_template("journal.html")
	return HttpResponse(template.render())
	#return HttpResponse(template.render()

def configure(request):
	template = loader.get_template("configure.html")
	return HttpResponse(template.render())
	#return HttpResponse(template.render()


def polls_list(request):
    MAX_OBJECTS = 20
#    polls = Poll.objects.all()[:MAX_OBJECTS]
    data = {"results": list("Tni na pleten")}
    return JsonResponse(data)


def polls_detail(request, pk):
   # poll = get_object_or_404(Poll, pk=pk)
    data = {"results": {
        "question": "xxxx",
        "created_by": "Oleg",
        "pub_date": "yesterday"
    }}
    return JsonResponse(data)

# Возвращает последнии sec данных канала ch
def lastdata_view(request, ch, sec):
	end_time = datetime.datetime.now()	
	start_time = end_time - datetime.timedelta(seconds = sec)
	data = Curdata.objects.filter(time__range =(start_time,end_time)).filter(ch = ch)
	#data = Curdata.objects.all()[:10]

	print(data)
	res = {'result': list(data.values("c_avr", "c_max", "time", "ch")), "start":start_time, "endtime":end_time }
	return JsonResponse(res)