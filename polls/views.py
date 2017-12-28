import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from ipware.ip import get_ip
from .models import Question, Answer, UserQuestionAnswer
from .forms import QuestionForm

AMOUNT_OF_POLLS_TO_DISPLAY = 10
VOTING_NONREG_AMOUNT_OF_TIME = timezone.timedelta(seconds=15)
VOTING_NONREG_AMOUNT_OF_VOTES = 2


def poll_index(request):
    latest_polls = Question.objects.order_by('-pub_date')[:AMOUNT_OF_POLLS_TO_DISPLAY]
    for l in latest_polls:
        l.author = User.objects.filter(pk=l.user_id).first()

    return render(request, 'polls/poll_index.html', {'latest_question_list': latest_polls})


def create_poll(request):
    # creating a poll is not allowed to non-registered users
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
            return redirect('polls:poll_index')
        # else-branch omitted for redundancy
    else:
        form = QuestionForm()
    return render(request, 'polls/create_poll.html', {'form': form})


def view_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        # it doesn't matter whether question exists or not: in any case we are
        # rendering with the same variables set
        pass

    already_voted = has_user_already_voted(request, question)
    return render(request, 'polls/view_question.html', {'question': question, 'already_voted': already_voted})


def has_user_already_voted(request, question):
    if request.user.is_authenticated:
        already_voted = UserQuestionAnswer.objects.filter(voter=request.user).filter(question=question).exists()
    else:
        ip = get_ip(request)
        already_voted = len([uqa for uqa in UserQuestionAnswer.objects.filter(ip=ip).filter(question=question)
            if timezone.now() - uqa.date <= VOTING_NONREG_AMOUNT_OF_TIME]) >= VOTING_NONREG_AMOUNT_OF_VOTES
    return already_voted


def vote(request, question_id):
    if not Question.objects.filter(pk=question_id).exists():
        return render(request, 'polls/results.html')

    q = Question.objects.get(pk=question_id)
    if has_user_already_voted(request, q):
        return results(request, question_id)

    if not q.multiple_choice:
        answer = Answer.objects.get(pk=request.POST['answer'])
        if not answer:
            logging.getLogger(__name__).error('\nANSWER IS NONE\n')
            raise Exception
        else:
            # here was the debugging info
            # logging.getLogger(__name__).error('\nANSWER IS {}\n'.format(answer.__str__()))
            pass

        if request.user.is_authenticated:
            UserQuestionAnswer.objects.create(voter=request.user, question=q, answer=answer, date=timezone.now())
        else:
            UserQuestionAnswer.objects.create(ip=get_ip(request), question=q, answer=answer, date=timezone.now())

        answer.votes = UserQuestionAnswer.objects.filter(answer=answer).count()
        answer.save()
    else:
        # multiple choice feature is not implemented
        pass

    return results(request, question_id)


def results(request, question_id):
    # template handles none-values on question, just pass
    if not Question.objects.filter(pk=question_id).exists():
        return render(request, 'polls/results.html')

    question = Question.objects.get(pk=question_id)

    # counting total votes on current poll (probably should be refactored as separate method)
    votes_total = 0
    for a in question.answer_set.all():
        votes_total += a.votes

    return render(request, 'polls/results.html', {'question': question, 'votes_total': votes_total})
