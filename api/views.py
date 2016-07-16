from django.http import HttpResponse
import datetime
import json
from django.http import HttpResponseRedirect
import pokelocator_api

def json_custom_parser(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        dot_ix = 19
        return obj.isoformat()[:dot_ix]
    else:
        raise TypeError(obj)


def get_poke(request):

    location = request.POST.get('location', "911 Washington Ave, Saint Louis, MO")
    result = pokelocator_api.main(location=location)
    
    return HttpResponse(json.dumps({
        "status": "success",
        "data": result
    }, default=json_custom_parser), content_type='application/json', status=200)
    
    
def load_frontend(request):
    return HttpResponseRedirect("/static/index.html")

