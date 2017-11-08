# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import socket
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from .models import *

from serialcontrol import SerialControl
import settings

control = SerialControl(settings.IRCONTROL_PORT, settings.IRCONTROL_BAUD_RATE)

def get_ip_addr(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_host(request):
    ip = get_ip_addr(request)
    if not ip:
        return None
    d = socket.gethostbyaddr(ip)
    if d:
        return d[0]

def index(request):
    commands = IrCommand.objects.all()
    context = {
        'commands' : commands,
    }
    return render(request, 'ircontrol/index.html', context)
    
def blamelist(request):
    blamelist = CommandLogEntry.objects.all().order_by('when')[::-1][:10]
    context = {
        'blamelist' : blamelist
    }
    return render(request, 'ircontrol/blamelist.html', context)

def measure_temp(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed("Method not allowed")
    result = control.measure_temp()
    return JsonResponse({
        'result': result[0],
        'error' : result[1],
        'temp' : result[2]
    })

@csrf_exempt    
def execute_command(request, id):
    if request.method != 'POST':
        return HttpResponseNotAllowed("Method not allowed")
    try:
        command = IrCommand.objects.get(id=id)
    except ObjectDoesNotExist as ex:
        return JsonResponse({'result': 404, "error": "No command with id %s found" % id})
    
    result = control.execute(command.frequency, command.command)
    
    if result[0] == 0:
        command_log = CommandLogEntry(executor=get_ip_addr(request), host=get_client_host(request), when=datetime.now(), command=command)
        command_log.save()
    
    return JsonResponse({
        'result': result[0],
        'error': result[1]
    })
