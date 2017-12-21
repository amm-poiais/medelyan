from django import template
import re


register = template.Library()

@register.simple_tag(takes_context=True)
def current_user(context):
    request = context['request']
    if not request.user.is_authenticated:
        return 'Not logged in'
    elif re.match('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', request.user.username):
        return 'Temporarily logged in as {}'.format(request.user.username)
    else:
        return 'Logged in as {}'.format(request.user.username)
