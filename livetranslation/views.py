from django.http import HttpResponse
from django.utils import simplejson
from livetranslation.forms import extract_form_data
from livetranslation.translation import (
    PoFileSession, get_all_translations, save_translations)


def get_translations(request):
    """
    Remember to encode quotes as html entities!
    """
    if request.method == 'POST':
        data = extract_form_data(request.POST)
        save_translations(data, PoFileSession())
        return HttpResponse('OK')
    else:
        response = get_all_translations(request.GET['msgid'],
                                        request.GET.get('msgid_plural'))
        return HttpResponse(simplejson.dumps(response),
                            content_type='application/json')

