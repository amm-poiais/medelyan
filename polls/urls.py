from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('<int:question_id>/results', views.results, name='results'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path('<int:question_id>/view', views.view_question, name='view_question'),
    path('create_poll/', views.create_poll, name='create_poll'),
    path('', views.poll_index, name='poll_index'),
]
