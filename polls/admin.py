from django.contrib import admin
from .models import Question
from .models import UserQuestionAnswer


admin.site.register(Question)
admin.site.register(UserQuestionAnswer)