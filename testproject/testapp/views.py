from django.shortcuts import render_to_response
from livetranslation import ugettext as _


def frontpage(request):
    return render_to_response(
        'testapp/frontpage.html',
        {'translated': _(
            u"This is the value of context['translated'].")})
