# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone

from socialnetwork.forms import RegistrationForm, CommentPost



@login_required
def home(request):
	#Demonstrate a post in global stream
	entry = Fist_Entry
	#fill in dummy time and user data
	entry['created_by']    = request.user
	entry['creation_time'] = timezone.now()
	entry['updated_by']    = request.user
	entry['update_time']  = timezone.now()

	form = CommentPost(entry)
	context = {'entry': entry, 'form:':form}
	return render(request, 'socialnetwork/global.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def follower (request):
	#Demonstrate a post in global stream
	entry = Second_Entry
	#fill in dummy time and user data
	entry['created_by']    = request.user
	entry['creation_time'] = timezone.now()
	entry['updated_by']    = request.user
	entry['update_time']  = timezone.now()

	form = CommentPost(entry)
	context = {'entry': entry, 'form:':form}
	return render(request, 'socialnetwork/follower.html', context)


Fist_Entry = {
	'id': 1,
    'text': "You are being watched. The government has a secret system. A machine.It spies on you every hour of every day.I know because I built it. I designed the machine to detect acts of terror,But it sees everything. Violent crimes involving ordinary people.People like you.Crimes the government considered irrelevant.They wouldn't act, so I decided I would.But I needed a partner.Someone with the skills to intervene.Hunted by the authorities, we work in secret.You'll never find us.But victim or perpetrator, if your number's up,we'll find you. ",
}


Second_Entry = {
	'id': 2,
    'text': 'The Three Laws of Robotics: 1. A robot may not injure a human being or, through inaction, allow a human being to come to harm. 2. A robot must obey the orders given it by human beings except where such orders would conflict with the First Law. 3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws.',
}


