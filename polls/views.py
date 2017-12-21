from django.shortcuts import render, redirect
from .models import Question
from .forms import QuestionForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from ipware.ip import get_ip
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
import logging


def poll_index(request):
    latest = Question.objects.order_by('-pub_date')[:10]
    for l in latest:
        l.author = User.objects.filter(pk=l.user_id).first()
    return render(request, 'polls/poll_index.html', {'latest_question_list': latest})

def create_poll(request):
    logger = logging.getLogger(__name__)
    # assure that there's a valid user
    user = None
    if not request.user.username:
        ip = get_ip(request)
        # it's ok with ip
        if ip is not None:
            name = ip
            # there's no such a user?
            if not User.objects.filter(username=name).exists():
                # create one
                user = User.objects.create_user(username=name, password=name)
                if user is None:
                    logger.error('\ncan\'t create user\n')
                else:
                    logger.error('User created')
            else:
                # else get him!
                user = User.objects.get(username=name)
                if user is None:
                    logger.error('\ncan\'t get user with ip {}\n'.format(name))
                else:
                    logger.error('User found')
        else:
            logger.error('\nno ip?\n')

        logger.error('\nReached: {} - {}\n'.format(user.username, user.password))
        user = authenticate(username=name, password=name)
        if user is None:
            logger.error('\nuser is none after authentication attempt\n')
        login(request, user)
    else:
        messages.error(request, 'Sorry, but we cannot obtain ur ip. Hence you are not allowed'
                                'to vote yet. Please, for more information contact developer')
        redirect('/')

    # fill new question fields
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question()
            q.text = form.cleaned_data['text']
            q.multiple_choice = form.cleaned_data['multiple_choice']
            q.user = User.objects.get(username=request.user.username)
            q.pub_date = timezone.now()
            q.save()
            messages.success(request, 'Poll created!')
            return redirect('polls:poll_index')
    else:
        form = QuestionForm()
    return render(request, 'polls/create_poll.html', {'form': form})
