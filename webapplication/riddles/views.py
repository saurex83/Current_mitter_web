from django.http import HttpResponse
from django.template import Context, loader
from django import template
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import datetime
from .models import Curdata,Cnf

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


# Ищем максимальное значение среднего тока в запрошенных данных
def find_max_current(data, ch):
	maximum = {'time' : '', 'value' : -1}
	for i in data:
		if i['ch'] != ch:
			continue
		if i['c_avr'] > maximum['value']:
			maximum['value'] = i['c_avr']
			maximum['time'] = i['time']
	return maximum


# Возвращает последнии sec данных трех каналов
def lastdata_view(request, sec):
	end_time = datetime.datetime.now()	
	start_time = end_time - datetime.timedelta(seconds = sec)
	
	# Подгружаем данные из временного диапазон
	data = Curdata.objects.filter(time__range =(start_time,end_time))
	
	# Загружаем настройки
	config = Cnf.objects.all()


	lables = list()
	ch1_avr = list()
	ch2_avr = list()
	ch3_avr = list()
	ch1_max = list()
	ch2_max = list()
	ch3_max = list()

	data = list(data.values("time", "ch", "c_avr", "c_max"))

	for i in data:
		if i['ch'] == 1:
			time = i['time']
			time = time.strftime("%H:%M:%S")
			lables.append(time)
			ch1_avr.append(i["c_avr"])
			ch1_max.append(i["c_max"])
		if i['ch'] == 2:
			ch2_avr.append(i["c_avr"])
			ch2_max.append(i["c_max"])
		if i['ch'] == 3:
			ch3_avr.append(i["c_avr"])
			ch3_max.append(i["c_max"])

	res = {
		'labels':lables, 'ch1_avr':ch1_avr, 
		'ch2_avr':ch2_avr, 'ch3_avr':ch3_avr, 
		'ch1_max' :ch1_max, 'ch2_max' :ch2_max,
		'ch3_max':ch3_max,
		'ch1_avr_now' : ch1_avr[-1],
		'ch2_avr_now' : ch2_avr[-1],
		'ch3_avr_now' : ch3_avr[-1],
		'ch1_pic_now' : ch1_max[-1],
		'ch2_pic_now' : ch2_max[-1],
		'ch3_pic_now' : ch3_max[-1],
		'ch1_max_val' :find_max_current(data, 1),
		'ch2_max_val' :find_max_current(data, 2),
		'ch3_max_val' :find_max_current(data, 3)
		}
	return JsonResponse(res)