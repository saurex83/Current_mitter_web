from django.http import HttpResponse
from django.template import Context, loader
from django import template
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import datetime
import calendar
from .models import Curdata,Cnf,Journal
import json
from jsonschema import validate,ValidationError
import subprocess
from django.core.exceptions import ObjectDoesNotExist

PARAMS_DEFAULT = {"MAX_CURR_CH1" : "50", "MAX_CURR_CH2" : "50",
					"MAX_CURR_CH3" : "50", "MAX_TIME_CH1" : "3",
					"MAX_TIME_CH2" : "3", "MAX_TIME_CH3" : "3",
					"NAME_CH1" : "Фаза 1",
					"NAME_CH2" : "Фаза 2", "NAME_CH3" : "Фаза 3",
					"NAME_OBJ" : "Помещение 1" }

CLEAN_PASS = "mittermitter"

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

def set_time(request,json_data):
	res = {'result' : True}

	# На расбери нужно установить ntp сервер и отключить его.
	# в противном случаи время устанавливаться не будет
	try:
		json_data = json.loads(json_data)

		date = json_data['date']
		hour = int(json_data['hour'])
		minute = int(json_data['min'])
		seconds = int(json_data['sec'])

		time = datetime.datetime.strptime(date,'%d.%m.%Y')
		time = time.replace(hour = hour, minute = minute, second = seconds)
	except ValueError:
		res['result'] = False
		res['msg'] = 'Данные введены с ошибкой'
		return JsonResponse(res)

	set_date = time.strftime('%Y%m%d')
	print(set_date)

	set_time = time.strftime('%H:%M:%S')

	code = subprocess.call("date +%Y%m%d -s " + '"' + set_date + '"',shell=True )
	if (code ==0):
		print ("дата изменена")

	code = subprocess.call("date +%T -s " + '"' + set_time + '"' ,shell=True)
	if (code ==0):
		print ("Время изменено")

	code = subprocess.call("hwclock -w" ,shell=True)



	return JsonResponse({'result':True})

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

# Загружаем настройки из базы данных, либо устанавливаем по умолчанию
def update_params():
	PARAMS = PARAMS_DEFAULT

	# Загружаем настройки
	config = Cnf.objects.all()
	config = list(config.values("name", "value"))
	
	for item in config:
		PARAMS[item['name']] = item['value']

	return(PARAMS)


def trunc_tables(request, password):
	if (password != CLEAN_PASS):
		return JsonResponse({'result' : False})
			
	Cnf.objects.all().delete()
	Curdata.objects.all().delete()
	Journal.objects.all().delete()
	return JsonResponse({'result' : True})


def get_alarm(request):
	# Уровни журнала
	J_INFO = 0
	J_WARNING = 1
	J_ALARM = 2
	ALARM_TIME = 5

	try:
		journal_data = Journal.objects.latest("id")
	#journal_data = list(journal_data.values("id", "time", "errlevel", "errleveltext", "source", "message"))
	except ObjectDoesNotExist:
		return JsonResponse({'isAlarm' : False})

	if (journal_data.errlevel != J_ALARM):
		return JsonResponse({'isAlarm' : False})

	time = datetime.datetime.now()
	rec_time = journal_data.time
	time_delta = (time-rec_time).seconds

	if (time_delta > ALARM_TIME):
		return JsonResponse({'isAlarm' : False})

	res = dict()
	res['isAlarm'] = True
	res['src'] =  journal_data.source
	res['time'] =  journal_data.time.strftime("%d/%m/%y %H:%M:%S")
	res['msg'] =  journal_data.message

	return JsonResponse(res)

def get_cfn_names(request):
	params =  update_params()
	return JsonResponse(params)

def check_value(text_val, min_val, max_val):
	try:
		val = int(text_val)
	except ValueError:
		return False

	if (val >= min_val and val<=max_val):
 		return True

	return False

def update_db_value(name, val):
	print (name)
	db_obj, created = Cnf.objects.get_or_create(name = name,defaults={'name':name, 'value': val})
	db_obj.value = val
	db_obj.save()

def write_cfn_names(request,json_data):
	res = {'result' : True}
	try:
		data = json.loads(json_data)
	except ValueError:
		res['result'] = False
		res['msg'] = "Формат не json"
		return JsonResponse(res)

	schema = {
	    "type" : "object",
	    "required" : [
	    	"MAX_CURR_CH1",
	    	"MAX_CURR_CH2",
	    	"MAX_CURR_CH3",
	    	"MAX_TIME_CH1",
	    	"MAX_TIME_CH2",
	    	"MAX_TIME_CH3",
	    	"NAME_CH1",
	    	"NAME_CH2",
	    	"NAME_CH3",
	    	"NAME_OBJ"  
	    ],
	    "properties" : {
	        "MAX_CURR_CH1" : {"type" : "string"},
	        "MAX_CURR_CH2" : {"type" : "string"},
	        "MAX_CURR_CH3" : {"type" : "string"},
	        "MAX_TIME_CH1" : {"type" : "string"},
	        "MAX_TIME_CH2" : {"type" : "string"},
	        "MAX_TIME_CH3" : {"type" : "string"},
	        "NAME_CH1" : {"type" : "string"},
	        "NAME_CH2" : {"type" : "string"},
	        "NAME_CH3" : {"type" : "string"},
	        "NAME_OBJ" : {"type" : "string"}
	    },
	}
	
	try:
		validate(instance=data, schema=schema)
	except ValidationError as msg:
		res['result'] = False
		res['msg'] = str(msg)
		return JsonResponse(res)

	# так как мы работаем со строками, нужно проверить допустимы значения вручную 
	flag = True
	flag = flag and check_value(data['MAX_CURR_CH1'] , 1,1000)
	flag = flag and check_value(data['MAX_CURR_CH2'] , 1,1000)
	flag = flag and check_value(data['MAX_CURR_CH3'] , 1,1000)

	flag = flag and check_value(data['MAX_TIME_CH1'] , 1,120)
	flag = flag and check_value(data['MAX_TIME_CH2'] , 1,120)
	flag = flag and check_value(data['MAX_TIME_CH3'] , 1,120)

	if (flag == False):
		res['result'] = False
		res['msg'] = 'Неверное значение параметра'
		return JsonResponse(res)

	update_db_value('MAX_CURR_CH1', data['MAX_CURR_CH1'])
	update_db_value('MAX_CURR_CH2', data['MAX_CURR_CH2'])
	update_db_value('MAX_CURR_CH3', data['MAX_CURR_CH3'])

	update_db_value('MAX_TIME_CH1', data['MAX_TIME_CH1'])
	update_db_value('MAX_TIME_CH2', data['MAX_TIME_CH2'])
	update_db_value('MAX_TIME_CH3', data['MAX_TIME_CH3'])


	update_db_value('NAME_CH1', data['NAME_CH1'])
	update_db_value('NAME_CH2', data['NAME_CH2'])
	update_db_value('NAME_CH3', data['NAME_CH3'])
	update_db_value('NAME_OBJ', data['NAME_OBJ'])

	return JsonResponse(res)

def get_journal_n(request,n):
	journal_data = Journal.objects.order_by('-id')[:n]
	journal_data = list(journal_data.values("id", "time", "errlevel", "errleveltext", "source", "message"))

	res = []
	for item in journal_data:
		row = list()
		row.append(item['id'])
		row.append(item['errleveltext'])
		row.append(item['time'].strftime("%d/%m/%y %H:%M:%S"))
		row.append(item['source'])
		row.append(item['message'])
		res.append(row)

	return JsonResponse({'data':res})

def get_journal(request):
	journal_data = Journal.objects.all()
	journal_data = list(journal_data.values("id", "time", "errlevel", "errleveltext", "source", "message"))

	res = []
	for item in journal_data:
		row = list()
		row.append(item['id'])
		row.append(item['errleveltext'])
		row.append(item['time'].strftime("%d/%m/%y %H:%M:%S"))
		row.append(item['source'])
		row.append(item['message'])
		res.append(row)

	return JsonResponse({'data':res})


def lastdata_view_1month(request):
	""" Возвращаем данные усредненные к 10 минутам """
	time = datetime.datetime.now()
	
	# Устанавливаем на начало месяца
	time = time.replace(day = 1, hour = 0, minute = 0,second = 0, microsecond = 0)
	# Количество дней в месяце
	days = calendar.monthrange(time.year, time.month)[1]
	#hour_cnt = days*24 # Количество часов в месяце

	min60 = datetime.timedelta(days = 1)
	time -=min60
	time_range = list()
	
	res = { 'labels' : [] , 'ch1_avr' : [], 'ch2_avr' : [], 'ch3_avr' : [],
	'ch1_max' : [], 'ch2_max' : [], 'ch3_max' : []}


	# Перебираем все часы в месяце
	for i in range(0,days):
		time_range.append({'end' : time+min60, 'start' : time })
		time = time + min60

	# загружаем данные соответсвующие временным отрезкам
	for ti in time_range:
		st = ti['start']
		en = ti['end']
		data = Curdata.objects.filter(time__range =(st,en))
		data = list(data.values("ch", "c_avr", "c_max"))
		# усредняем полученные данные
		tmp_c1_avr = 0;
		tmp_c2_avr = 0;
		tmp_c3_avr = 0;
		tmp_c1_max = 0;
		tmp_c2_max = 0;
		tmp_c3_max = 0;

		cnt = 0 # количество измерений
		for i in data:
			cnt += 1
			if i['ch'] == 1:
				tmp_c1_avr += i['c_avr']
				tmp_c1_max += i['c_max']
			if i['ch'] == 2:
				tmp_c2_avr += i['c_avr']
				tmp_c2_max += i['c_max']
			if i['ch'] == 3:
				tmp_c3_avr += i['c_avr']
				tmp_c3_max += i['c_max']

		if cnt !=0 :
			tmp_c1_avr = tmp_c1_avr / cnt
			tmp_c2_avr = tmp_c2_avr / cnt
			tmp_c3_avr = tmp_c3_avr / cnt
			tmp_c1_max = tmp_c1_max / cnt
			tmp_c2_max = tmp_c2_max / cnt
			tmp_c3_max = tmp_c3_max / cnt

		res['ch1_avr'].append(tmp_c1_avr)
		res['ch2_avr'].append(tmp_c2_avr)
		res['ch3_avr'].append(tmp_c3_avr)
		res['ch1_max'].append(tmp_c1_max)
		res['ch2_max'].append(tmp_c2_max)
		res['ch3_max'].append(tmp_c3_max)
		res['labels'].append(en.strftime("%d/%m/%y"))
		#res['labels'].append(en.strftime("%d/%m/%y"))

		params = update_params()
		res['MAX_CURR_CH1'] = float(params['MAX_CURR_CH1'])
		res['MAX_CURR_CH2'] = float(params['MAX_CURR_CH2'])
		res['MAX_CURR_CH3'] = float(params['MAX_CURR_CH3'])
		res['NAME_CH1'] =  params['NAME_CH1']
		res['NAME_CH2'] = params['NAME_CH2']
		res['NAME_CH3'] = params['NAME_CH3']
		res['NAME_OBJ'] = params['NAME_OBJ']
		
	##print(time_range)
	#res = {"timei" : time_range}
	return JsonResponse(res)

def lastdata_view_1day(request):
	""" Возвращаем данные усредненные к 10 минутам """
	time = datetime.datetime.now()
	
	# Устанавливаем на начало дня
	time = time.replace(hour = 0, minute = 0,second = 0, microsecond = 0)

	min10 = datetime.timedelta(seconds = 600)

	time_range = list()
	
	res = { 'labels' : [] , 'ch1_avr' : [], 'ch2_avr' : [], 'ch3_avr' : [],
	'ch1_max' : [], 'ch2_max' : [], 'ch3_max' : []}


	# В сутках всего 144 дисятиминутных интервалом
	for i in range(0,144):
		time_range.append({'end' : time+min10, 'start' : time })
		time = time + min10

	# загружаем данные соответсвующие временным отрезкам
	for ti in time_range:
		st = ti['start']
		en = ti['end']
		data = Curdata.objects.filter(time__range =(st,en))
		data = list(data.values("ch", "c_avr", "c_max"))
		# усредняем полученные данные
		tmp_c1_avr = 0;
		tmp_c2_avr = 0;
		tmp_c3_avr = 0;
		tmp_c1_max = 0;
		tmp_c2_max = 0;
		tmp_c3_max = 0;

		cnt = 0 # количество измерений
		for i in data:
			cnt += 1
			if i['ch'] == 1:
				tmp_c1_avr += i['c_avr']
				tmp_c1_max += i['c_max']
			if i['ch'] == 2:
				tmp_c2_avr += i['c_avr']
				tmp_c2_max += i['c_max']
			if i['ch'] == 3:
				tmp_c3_avr += i['c_avr']
				tmp_c3_max += i['c_max']

		if cnt !=0 :
			tmp_c1_avr = tmp_c1_avr / cnt
			tmp_c2_avr = tmp_c2_avr / cnt
			tmp_c3_avr = tmp_c3_avr / cnt
			tmp_c1_max = tmp_c1_max / cnt
			tmp_c2_max = tmp_c2_max / cnt
			tmp_c3_max = tmp_c3_max / cnt

		res['ch1_avr'].append(tmp_c1_avr)
		res['ch2_avr'].append(tmp_c2_avr)
		res['ch3_avr'].append(tmp_c3_avr)
		res['ch1_max'].append(tmp_c1_max)
		res['ch2_max'].append(tmp_c2_max)
		res['ch3_max'].append(tmp_c3_max)
		#res['labels'].append(en)
		res['labels'].append(en.strftime("%H:%M"))

		params = update_params()
		res['MAX_CURR_CH1'] = float(params['MAX_CURR_CH1'])
		res['MAX_CURR_CH2'] = float(params['MAX_CURR_CH2'])
		res['MAX_CURR_CH3'] = float(params['MAX_CURR_CH3'])
		res['NAME_CH1'] =  params['NAME_CH1']
		res['NAME_CH2'] = params['NAME_CH2']
		res['NAME_CH3'] = params['NAME_CH3']
		res['NAME_OBJ'] = params['NAME_OBJ']
		
	##print(time_range)
	#res = {"timei" : time_range}
	return JsonResponse(res)

def lastdata_view_aver_1min(request, minute):
	""" Возвращаем данные усредненные к 1 минуте """
	time = datetime.datetime.now()
	
	# Округлим текущее время до минуты
	time = time.replace(second = 0, microsecond = 0)
	min1 = datetime.timedelta(seconds = 60)

	time_range = list()
	
	res = { 'labels' : [] , 'ch1_avr' : [], 'ch2_avr' : [], 'ch3_avr' : [],
	'ch1_max' : [], 'ch2_max' : [], 'ch3_max' : []}


	# Формируем поминутный список интервалов времени
	for i in range(0,minute):
		time_range.append({'end' : time, 'start' : time-min1 })
		time = time -min1

	# загружаем данные соответсвующие временным отрезкам
	for ti in time_range:
		st = ti['start']
		en = ti['end']
		data = Curdata.objects.filter(time__range =(st,en))
		data = list(data.values("ch", "c_avr", "c_max"))
		# усредняем полученные данные
		tmp_c1_avr = 0;
		tmp_c2_avr = 0;
		tmp_c3_avr = 0;
		tmp_c1_max = 0;
		tmp_c2_max = 0;
		tmp_c3_max = 0;

		cnt = 0 # количество измерений
		for i in data:
			cnt += 1
			if i['ch'] == 1:
				tmp_c1_avr += i['c_avr']
				tmp_c1_max += i['c_max']
			if i['ch'] == 2:
				tmp_c2_avr += i['c_avr']
				tmp_c2_max += i['c_max']
			if i['ch'] == 3:
				tmp_c3_avr += i['c_avr']
				tmp_c3_max += i['c_max']

		if cnt !=0 :
			tmp_c1_avr = tmp_c1_avr / cnt
			tmp_c2_avr = tmp_c2_avr / cnt
			tmp_c3_avr = tmp_c3_avr / cnt
			tmp_c1_max = tmp_c1_max / cnt
			tmp_c2_max = tmp_c2_max / cnt
			tmp_c3_max = tmp_c3_max / cnt

		res['ch1_avr'].insert(0,tmp_c1_avr)
		res['ch2_avr'].insert(0,tmp_c2_avr)
		res['ch3_avr'].insert(0,tmp_c3_avr)
		res['ch1_max'].insert(0,tmp_c1_max)
		res['ch2_max'].insert(0,tmp_c2_max)
		res['ch3_max'].insert(0,tmp_c3_max)
		res['labels'].insert(0,en.strftime("%H:%M"))

		#res['ch1_avr'].reverse()
		#res['ch2_avr'].reverse()
	#	res['ch3_avr'].reverse()
	#	res['ch1_max'].reverse()
	#	res['ch2_max'].reverse()
	#	res['ch3_max'].reverse()
	#	res['labels'].reverse()

		
		params = update_params()
		res['MAX_CURR_CH1'] = float(params['MAX_CURR_CH1'])
		res['MAX_CURR_CH2'] = float(params['MAX_CURR_CH2'])
		res['MAX_CURR_CH3'] = float(params['MAX_CURR_CH3'])
		res['NAME_CH1'] =  params['NAME_CH1']
		res['NAME_CH2'] = params['NAME_CH2']
		res['NAME_CH3'] = params['NAME_CH3']
		res['NAME_OBJ'] = params['NAME_OBJ']
		
	##print(time_range)
	#res = {"timei" : time_range}
	return JsonResponse(res)

def lastdata_view_from_1day(request,t_date):
	""" Возвращаем данные усредненные к 10 минутам """
	time = datetime.datetime.strptime(t_date,'%d.%m.%Y %H:%M')

	# Устанавливаем на начало дня
	time = time.replace(hour = 0, minute = 0,second = 0, microsecond = 0)

	min10 = datetime.timedelta(seconds = 600)

	time_range = list()
	
	res = { 'labels' : [] , 'ch1_avr' : [], 'ch2_avr' : [], 'ch3_avr' : [],
	'ch1_max' : [], 'ch2_max' : [], 'ch3_max' : []}


	# В сутках всего 144 дисятиминутных интервалом
	for i in range(0,144):
		time_range.append({'end' : time+min10, 'start' : time })
		time = time + min10

	# загружаем данные соответсвующие временным отрезкам
	for ti in time_range:
		st = ti['start']
		en = ti['end']
		data = Curdata.objects.filter(time__range =(st,en))
		data = list(data.values("ch", "c_avr", "c_max"))
		# усредняем полученные данные
		tmp_c1_avr = 0;
		tmp_c2_avr = 0;
		tmp_c3_avr = 0;
		tmp_c1_max = 0;
		tmp_c2_max = 0;
		tmp_c3_max = 0;

		cnt = 0 # количество измерений
		for i in data:
			cnt += 1
			if i['ch'] == 1:
				tmp_c1_avr += i['c_avr']
				tmp_c1_max += i['c_max']
			if i['ch'] == 2:
				tmp_c2_avr += i['c_avr']
				tmp_c2_max += i['c_max']
			if i['ch'] == 3:
				tmp_c3_avr += i['c_avr']
				tmp_c3_max += i['c_max']

		if cnt !=0 :
			tmp_c1_avr = tmp_c1_avr / cnt
			tmp_c2_avr = tmp_c2_avr / cnt
			tmp_c3_avr = tmp_c3_avr / cnt
			tmp_c1_max = tmp_c1_max / cnt
			tmp_c2_max = tmp_c2_max / cnt
			tmp_c3_max = tmp_c3_max / cnt

		res['ch1_avr'].append(tmp_c1_avr)
		res['ch2_avr'].append(tmp_c2_avr)
		res['ch3_avr'].append(tmp_c3_avr)
		res['ch1_max'].append(tmp_c1_max)
		res['ch2_max'].append(tmp_c2_max)
		res['ch3_max'].append(tmp_c3_max)
		#res['labels'].append(en)
		res['labels'].append(en.strftime("%H:%M"))

		params = update_params()
		res['MAX_CURR_CH1'] = float(params['MAX_CURR_CH1'])
		res['MAX_CURR_CH2'] = float(params['MAX_CURR_CH2'])
		res['MAX_CURR_CH3'] = float(params['MAX_CURR_CH3'])
		res['NAME_CH1'] =  params['NAME_CH1']
		res['NAME_CH2'] = params['NAME_CH2']
		res['NAME_CH3'] = params['NAME_CH3']
		res['NAME_OBJ'] = params['NAME_OBJ']
		
	##print(time_range)
	#res = {"timei" : time_range}
	return JsonResponse(res)

def lastdata_view_aver_1min_from_time(request, minute, t_date):
	""" Возвращаем данные усредненные к 1 минуте начиная с времени from_time"""
	time = datetime.datetime.strptime(t_date,'%d.%m.%Y %H:%M')
	
	# Округлим текущее время до минуты
	time = time.replace(second = 0, microsecond = 0)
	min1 = datetime.timedelta(seconds = 60)

	time_range = list()
	
	res = { 'labels' : [] , 'ch1_avr' : [], 'ch2_avr' : [], 'ch3_avr' : [],
	'ch1_max' : [], 'ch2_max' : [], 'ch3_max' : []}


	# Формируем поминутный список интервалов времени
	for i in range(0,minute):
		time_range.append({'end' : time, 'start' : time-min1 })
		time = time -min1

	# загружаем данные соответсвующие временным отрезкам
	for ti in time_range:
		st = ti['start']
		en = ti['end']
		data = Curdata.objects.filter(time__range =(st,en))
		data = list(data.values("ch", "c_avr", "c_max"))
		# усредняем полученные данные
		tmp_c1_avr = 0;
		tmp_c2_avr = 0;
		tmp_c3_avr = 0;
		tmp_c1_max = 0;
		tmp_c2_max = 0;
		tmp_c3_max = 0;

		cnt = 0 # количество измерений
		for i in data:
			cnt += 1
			if i['ch'] == 1:
				tmp_c1_avr += i['c_avr']
				tmp_c1_max += i['c_max']
			if i['ch'] == 2:
				tmp_c2_avr += i['c_avr']
				tmp_c2_max += i['c_max']
			if i['ch'] == 3:
				tmp_c3_avr += i['c_avr']
				tmp_c3_max += i['c_max']

		if cnt !=0 :
			tmp_c1_avr = tmp_c1_avr / cnt
			tmp_c2_avr = tmp_c2_avr / cnt
			tmp_c3_avr = tmp_c3_avr / cnt
			tmp_c1_max = tmp_c1_max / cnt
			tmp_c2_max = tmp_c2_max / cnt
			tmp_c3_max = tmp_c3_max / cnt

		res['ch1_avr'].insert(0,tmp_c1_avr)
		res['ch2_avr'].insert(0,tmp_c2_avr)
		res['ch3_avr'].insert(0,tmp_c3_avr)
		res['ch1_max'].insert(0,tmp_c1_max)
		res['ch2_max'].insert(0,tmp_c2_max)
		res['ch3_max'].insert(0,tmp_c3_max)
		res['labels'].insert(0,en.strftime("%H:%M"))

		#res['ch1_avr'].reverse()
		#res['ch2_avr'].reverse()
	#	res['ch3_avr'].reverse()
	#	res['ch1_max'].reverse()
	#	res['ch2_max'].reverse()
	#	res['ch3_max'].reverse()
	#	res['labels'].reverse()

		
		params = update_params()
		res['MAX_CURR_CH1'] = float(params['MAX_CURR_CH1'])
		res['MAX_CURR_CH2'] = float(params['MAX_CURR_CH2'])
		res['MAX_CURR_CH3'] = float(params['MAX_CURR_CH3'])
		res['NAME_CH1'] =  params['NAME_CH1']
		res['NAME_CH2'] = params['NAME_CH2']
		res['NAME_CH3'] = params['NAME_CH3']
		res['NAME_OBJ'] = params['NAME_OBJ']
		
	##print(time_range)
	#res = {"timei" : time_range}
	return JsonResponse(res)


# Возвращает последнии sec данных трех каналов
def lastdata_view(request, sec):
	end_time = datetime.datetime.now()	
	start_time = end_time - datetime.timedelta(seconds = sec)
	
	# Подгружаем данные из временного диапазон
	data = Curdata.objects.filter(time__range =(start_time,end_time)).order_by('time')
	params = update_params()


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
		'ch3_max_val' :find_max_current(data, 3),
		'MAX_CURR_CH1' : float(params['MAX_CURR_CH1']),
		'MAX_CURR_CH2' : float(params['MAX_CURR_CH2']),
		'MAX_CURR_CH3' : float(params['MAX_CURR_CH3']),
		'NAME_CH1' : params['NAME_CH1'],
		'NAME_CH2' : params['NAME_CH2'],
		'NAME_CH3' : params['NAME_CH3'],
		'NAME_OBJ' : params['NAME_OBJ']
		}
	return JsonResponse(res)