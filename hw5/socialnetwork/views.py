# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.db import transaction

from socialnetwork.forms import *
from socialnetwork.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404


@login_required
def home(request):
    entry = Fist_Entry
    # fill in dummy time and user data
    entry['created_by']    = request.user
    entry['creation_time'] = timezone.now()
    entry['updated_by']    = request.user
    entry['update_time']  = timezone.now()

    form = CommentPostForm(entry)
    posts = Post.objects.all().order_by("-creation_time")
    context = {'entry': entry, 'form:':form, 'posts':posts}

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

    # Create profile for user
    new_profile = Profile(user=new_user)
    new_profile.save()

    # Logs in the new user and redirects to homepage
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def follower (request):
    # Demonstrate a post in global stream
    entry = Second_Entry
    # fill in dummy time and user data
    entry['created_by']    = request.user
    entry['creation_time'] = timezone.now()
    entry['updated_by']    = request.user
    entry['update_time']  = timezone.now()
    form = CommentPostForm(entry)

    # get user's following list
    curr_profile = get_object_or_404(Profile,user=request.user)
    follows = curr_profile.following.all()

    # get post of users the current user is following
    posts = Post.objects.filter(created_by__in=follows).order_by("-creation_time")
    context = {'entry': entry, 'form:':form, 'posts': posts, 'user': request.user, 'follows': follows}

    return render(request, 'socialnetwork/follower.html', context)


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    request_user_profile = get_object_or_404(Profile, user=request.user)
    curr_profile = get_object_or_404(Profile, user=profile_user)

    follows = request_user_profile.following.all();
    context = {'user' : profile_user, 'profile': curr_profile,  'follows': follows}

    # The profile is for the logged-in user
    if request.user.username == username:
        return render(request, 'socialnetwork/editProfile.html', context)

    # The profile page is for other users
    return render(request, 'socialnetwork/profile.html', context)


@login_required
@transaction.atomic
def edit(request):

    curr_profile = get_object_or_404(Profile, user=request.user)
    follows = curr_profile.following.all();

    if request.method == 'GET':
        form = ProfileForm()
        context = {'profile': curr_profile, 'form': form, 'follows': follows}

    else:
        curr_profile = Profile.objects.select_for_update().get(user=request.user)
        form = ProfileForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {'profile': curr_profile, 'form': form, 'follows': follows}

        else:
            # Set update user info, and save it!
            curr_profile.bio = form.cleaned_data['bio']
            if form.cleaned_data['picture']:
                curr_profile.picture = form.cleaned_data['picture']
                curr_profile.content_type = form.cleaned_data['picture'].content_type
            curr_profile.save();
            context = {'profile': curr_profile, 'form': form, 'follows': follows}

    return render(request, 'socialnetwork/editProfile.html', context)


@login_required
def get_photo(request, username):
    # get user
    user = get_object_or_404(User, username=username)
    curr_profile = get_object_or_404(Profile, user=user)

    if not curr_profile.picture:
        raise Http404

    return HttpResponse(curr_profile.picture, content_type=curr_profile.content_type)

@login_required
def post(request):
    posts = Post.objects.all().order_by("-creation_time")

    # no update if it is a get request
    if request.method == 'GET':
        context = {'posts': posts, 'form': PostForm()}
        return render(request, 'socialnetwork/global.html', context)

    form = PostForm(request.POST)
    # validate form.
    if not form.is_valid():
        context = {'posts': posts, 'form': form}
        return render(request, 'socialnetwork/global.html', context)

    # create a new post if valid
    new_post = Post(text=form.cleaned_data['text'], created_by=request.user)
    new_post.save()

    posts = Post.objects.all().order_by("-creation_time")
    context = {'posts': posts, 'form': PostForm()}
    return render(request, 'socialnetwork/global.html', context)


@login_required
def follow(request, username):
    # follow the profile user
    profile_user = get_object_or_404(User, username=username)
    curr_user_profile = Profile.objects.get(user=request.user)
    curr_user_profile.following.add(profile_user);
    curr_user_profile.save()

    # get return data
    profile_user_profile = Profile.objects.get(user=profile_user)
    follows = curr_user_profile.following.all()

    context = {'user': profile_user, 'profile': profile_user_profile, 'follows': follows}
    return render(request, 'socialnetwork/profile.html', context)


@login_required
def unfollow(request, username):
    # follow the profile user
    profile_user = get_object_or_404(User, username=username)
    curr_user_profile = Profile.objects.get(user=request.user)
    curr_user_profile.following.remove(profile_user);
    curr_user_profile.save()

    # get return data
    profile_user_profile = Profile.objects.get(user=profile_user)
    follows = curr_user_profile.following.all()

    context = {'user': profile_user, 'profile': profile_user_profile, 'follows': follows}
    return render(request, 'socialnetwork/profile.html', context)

Fist_Entry = {
	'id': 1,
    'text': "You are being watched. The government has a secret system. A machine.It spies on you every hour of every day.I know because I built it. I designed the machine to detect acts of terror,But it sees everything. Violent crimes involving ordinary people.People like you.Crimes the government considered irrelevant.They wouldn't act, so I decided I would.But I needed a partner.Someone with the skills to intervene.Hunted by the authorities, we work in secret.You'll never find us.But victim or perpetrator, if your number's up,we'll find you. ",
}


Second_Entry = {
	'id': 2,
    'text': 'The Three Laws of Robotics: 1. A robot may not injure a human being or, through inaction, allow a human being to come to harm. 2. A robot must obey the orders given it by human beings except where such orders would conflict with the First Law. 3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws.',
}



