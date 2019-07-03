from django.http import HttpResponse
from django.template import Context, loader
from django import template

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