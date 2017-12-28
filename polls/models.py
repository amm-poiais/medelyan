from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Question(models.Model):
    # we really need to know who created the question
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    text = models.CharField(max_length=50)
    pub_date = models.DateTimeField('published')
    multiple_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    # this one must be auto-calculated (see polls.views.vote method for details)
    votes = models.IntegerField('votes total', default=0)

    def __str__(self):
        return self.text


class UserQuestionAnswer(models.Model):
    # choice of registered users is remembered and stored in database
    # choice of non-registered users is remembered and stored also, but
    # their vote ability is limited to maximum of certain number per
    # some amount of time (see polls.views.hasUserAlreadyVoted method for details

    # who voted (for registered users)
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    # who voted (ip for non-registered users)
    ip = models.CharField(max_length=15, null=True)
    # what was the question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # what was the answer
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # where was the vote made
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        voter_name = self.voter.__str__() if self.voter is not None else self.ip;
        return '({}) {}: {} - {}'.format(self.date, voter_name, self.question.__str__(), self.answer.__str__())
