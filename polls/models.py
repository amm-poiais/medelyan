from django.contrib.auth import get_user_model
from django.db import models


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

    # this one must be auto-calculated
    votes = models.IntegerField('votes total', default=0)

    def __str__(self):
        return self.text


class UserQuestionAnswer(models.Model):
    # Need to check data uniqueness when user tries to vote - to prohibit multiply
    # votes on the same question (i.e. just check that the user hasn't voted for this question yet)
    # Thus, multiple choice is allowed in one vote request.

    # for non-registered user there will be behind-the-scene registration of temporary
    # user with user's ip as nick_name

    # who voted
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # what was the question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # what was the answer
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return '<not implemented>'
