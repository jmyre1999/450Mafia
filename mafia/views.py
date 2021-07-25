# This file is specifically for view functions (aka functions linked to urls)
# If you need to make a backend function, make it in utils.py and include it here

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse, Http404
from wsgiref.util import FileWrapper
from io import StringIO
from django.core.files.storage import default_storage
import os
from mafia.utils import *
from mafia import *
from django_ajax.decorators import ajax
from django.core.mail import send_mail
from django.conf import settings

def home(request):
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		contact = Contact.objects.create(name=name, email=email, subject=subject)
		if request.user.is_authenticated:
			contact.user = request.user
		contact.save()
		return HttpResponseRedirect('/')
	return render(request, "home.html")