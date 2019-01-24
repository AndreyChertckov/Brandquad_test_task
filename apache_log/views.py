from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from .models import Log


def search(get_parameters):
    logs = Log.objects.all()

    if 'ip' in get_parameters:
        logs = logs.filter(ip=get_parameters.get('ip'))
    if 'http_method' in get_parameters:
        logs = logs.filter(http_method=get_parameters.get('http_method'))
    if 'date' in get_parameters:
        logs = logs.filter(date=get_parameters.get('date'))
    if 'uri' in get_parameters:
        logs = logs.filter(uri=get_parameters.get('uri'))
    if 'status_code' in get_parameters:
        logs = logs.filter(status_code=get_parameters.get('status_code'))
    if 'size_of_response' in get_parameters:
        logs = logs.filter(
            size_of_response=get_parameters.get('size_of_response'))
    return logs


def get_page(request):

    logs = search(request.GET)

    paginator = Paginator(logs, 25)

    page = request.GET.get('page')
    print(page, flush=True)
    logs_page = paginator.get_page(page)
    response_dict = {'logs': list(map(model_to_dict, list(logs_page)))}
    if logs_page.has_previous():
        response_dict['previous'] = logs_page.previous_page_number()
    if logs_page.has_next():
        response_dict['next'] = logs_page.next_page_number()
    response_dict['last'] = paginator.num_pages
    return JsonResponse(response_dict, safe=False)


def get_info(request):
    logs = search(request.GET)
    data = dict()
    data['num_distinct_ips'] = logs.distinct('ip').count()
    data['num_distinct_http_method'] = logs.distinct('http_method').count()
    data['sum_response_size'] = logs.aggregate(Sum('response_size'))[
        'response_size__sum']
    data['most_common_ips'] = list(map(lambda l: l['ip'], logs.annotate(
        c=Count('ip')).distinct().order_by('-c').values('ip')[:10]))
    return JsonResponse(data)


def download_logs(request):
    logs = search(request.GET)
    labels = ['ip', 'date', 'http_method',
              'uri', 'status_code', 'response_size']
    wb = Workbook()
    ws = wb.active
    ws.title = 'logs'
    ws.append(labels)
    for l in logs:
        l_dict = model_to_dict(l)
        ws.append([l_dict[label] for label in labels])
    response = HttpResponse(save_virtual_workbook(wb), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'inline; filename=apache_log.xlsx'
    return response
