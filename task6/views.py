from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # automatic log in
            user = authenticate(username=username, password=password)
            poll_users_group = Group.objects.get(name='Poll Users')

            # group registration (by default for all users of site)
            # still not sure how this works;) - need more exploration
            # probably redundant
            user.groups.add(poll_users_group)
            poll_users_group.user_set.add(user)
            login(request, user)

            # go to home page
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
