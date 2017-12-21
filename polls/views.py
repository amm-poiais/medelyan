from django.shortcuts import render, redirect
from .models import Question, Answer, UserQuestionAnswer
from .forms import QuestionForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from ipware.ip import get_ip
from django.contrib import messages
from django.utils import timezone
import logging


def poll_index(request):
    latest = Question.objects.order_by('-pub_date')[:10]
    for l in latest:
        l.author = User.objects.filter(pk=l.user_id).first()
    return render(request, 'polls/poll_index.html', {'latest_question_list': latest})


def create_poll(request):
    # assure that there's a valid user
    if not request.user.is_authenticated:
        return redirect('polls:poll_index')

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


def view_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        pass

    already_voted = False;
    if request.user.is_authenticated:
        already_voted = UserQuestionAnswer.objects.filter(voter=request.user).filter(question=question).exists()
    else:
        # implement vote prohibition
        ip = get_ip(request)
        already_voted = len([uqa for uqa in UserQuestionAnswer.objects.filter(ip=ip).filter(question=question)
                         if timezone.now() - uqa.date <= timezone.timedelta(seconds=15)]) >= 1

    return render(request, 'polls/view_question.html', {'question': question, 'already_voted': already_voted})


def vote(request, question_id):
    if not Question.objects.filter(pk=question_id).exists():
        return render(request, 'polls/results.html')

    q = Question.objects.get(pk=question_id)

    if not q.multiple_choice:
        answer = Answer.objects.get(pk=request.POST['answer'])
        if not answer:
            logging.getLogger(__name__).error('\nANSWER IS NONE\n')
        else:
            logging.getLogger(__name__).error('\nANSWER IS {}\n'.format(answer.__str__()))

        if request.user.is_authenticated:
            UserQuestionAnswer.objects.create(voter=request.user, question=q, answer=answer, date=timezone.now())
        else:
            UserQuestionAnswer.objects.create(ip=get_ip(request), question=q, answer=answer, date=timezone.now())

        answer.votes = UserQuestionAnswer.objects.filter(answer=answer).count()
        answer.save()
    else:
        pass

    return results(request, question_id)


def results(request, question_id):
    if not Question.objects.filter(pk=question_id).exists():
        return render(request, 'polls/results.html')

    question = Question.objects.get(pk=question_id)
    votes_total = 0
    for a in question.answer_set.all():
        votes_total += a.votes

    return render(request, 'polls/results.html', {'question': question, 'votes_total': votes_total})
