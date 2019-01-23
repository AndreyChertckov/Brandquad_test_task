from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum, Count

from .models import Log


def get_page(request):

    logs = Log.objects.all()

    if 'ip' in request.GET:
        logs = logs.filter(ip = request.GET.get('ip'))
    if 'http_method' in request.GET:
        logs = logs.filter(http_method = request.GET.get('http_method'))
    if 'date' in request.GET:
        logs = logs.filter(date = request.GET.get('date'))
    if 'uri' in request.GET:
        logs = logs.filter(uri = request.GET.get('uri'))
    if 'status_code' in request.GET:
        logs = logs.filter(status_code = request.GET.get('status_code'))
    if 'size_of_response' in request.GET:
        logs = logs.filter(size_of_response = request.GET.get('size_of_response'))

    paginator = Paginator(logs, 25)

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


def get_info(request):
    logs = Log.objects.all()

    if 'ip' in request.GET:
        logs = logs.filter(ip = request.GET.get('ip'))
    if 'http_method' in request.GET:
        logs = logs.filter(http_method = request.GET.get('http_method'))
    if 'date' in request.GET:
        logs = logs.filter(date = request.GET.get('date'))
    if 'uri' in request.GET:
        logs = logs.filter(uri = request.GET.get('uri'))
    if 'status_code' in request.GET:
        logs = logs.filter(status_code = request.GET.get('status_code'))
    if 'size_of_response' in request.GET:
        logs = logs.filter(size_of_response = request.GET.get('size_of_response'))

    data = dict()
    data['num_distinct_ips'] = logs.distinct('ip').count()
    data['num_distinct_http_method'] = logs.distinct('http_method').count()
    data['sum_response_size'] = logs.aggregate(Sum('response_size'))['response_size__sum']
    data['most_common_ips'] = list(map(lambda l:l['ip'], logs.annotate(c=Count('ip')).distinct().order_by('-c').values('ip')[:10]))
    return JsonResponse(data)