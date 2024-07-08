# Email/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .task import test_func, send_mail_func

def test(request):
    test_func.delay()
    return HttpResponse('Test done!')

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("The mail is sent.Thank you.")
