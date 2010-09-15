from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from livetranslation.forms import extract_form_data
from livetranslation.translation import (
    PoFileSession, get_all_translations, save_translations)


def enable(request):
    request.session['livetranslation-enable'] = True
    return HttpResponseRedirect('/')


def disable(request):
    request.session['livetranslation-enable'] = False
    return HttpResponseRedirect('/')


def get_translations(request):
    """
    Remember to encode quotes as html entities!
    """
    if request.method == 'POST':
        data = extract_form_data(request.POST)
        save_translations(data, PoFileSession())
        return HttpResponse('OK', content_type='text/plain')
    else:
        response = get_all_translations(request.GET['msgid'],
                                        request.GET.get('msgid_plural'))
        return HttpResponse(simplejson.dumps(response),
                            content_type='application/json')

