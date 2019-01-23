from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from .models import Log


def get_page(request):

    logs = Log.objects.all()
    paginator = Paginator(logs, 50)

    page = request.GET.get('page')
    print(page, flush=True)
    logs_page = paginator.get_page(page)
    response_dict = {'logs':list(map(model_to_dict,list(logs_page)))}
    if logs_page.has_previous():
        response_dict['previous']= logs_page.previous_page_number()
    if logs_page.has_next():
        response_dict['next'] = logs_page.next_page_number()
    response_dict['last'] = paginator.num_pages
    return JsonResponse(response_dict, safe=False)
