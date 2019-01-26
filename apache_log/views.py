from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from .models import Log


def search(get_parameters):
    logs = Log.objects.get_queryset()

    if 'ip' in get_parameters:
        logs = logs.filter(ip=get_parameters.get('ip'))
    if 'http_method' in get_parameters:
        logs = logs.filter(http_method=get_parameters.get('http_method'))
    if 'start_date' in get_parameters:
        logs = logs.filter(date__gte=get_parameters.get('start_date'))
    if 'end_date' in get_parameters:
        logs = logs.filter(date__lte=get_parameters.get('end_date'))
    if 'uri' in get_parameters:
        logs = logs.filter(uri=get_parameters.get('uri'))
    if 'status_code' in get_parameters:
        logs = logs.filter(status_code=get_parameters.get('status_code'))
    if 'size_of_response' in get_parameters:
        logs = logs.filter(
            size_of_response=get_parameters.get('size_of_response'))
    return logs


def get_page(request):

    logs = search(request.GET).order_by('id')

    paginator = Paginator(logs, 25) # Make pages with 25 elements

    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    response_dict = {'logs': list(map(model_to_dict, list(logs_page)))}
    if logs_page.has_previous():
        response_dict['previous'] = logs_page.previous_page_number()
    if logs_page.has_next():
        response_dict['next'] = logs_page.next_page_number()
    response_dict['last'] = paginator.num_pages
    return JsonResponse(response_dict, safe=False) # return {'logs':[{'id':int,'ip':str,'date':datetime,'http_method':str,'uri':str,'status_code':str,'response_size':int},], 'previous':int, 'next':int,'last':int}


def get_info(request):
    logs = search(request.GET)
    data = dict()
    data['num_distinct_ips'] = logs.distinct('ip').count()
    data['num_distinct_http_methods'] = logs.distinct('http_method').count()
    data['sum_response_size'] = logs.aggregate(Sum('response_size'))[
        'response_size__sum']
    most_common_ips = logs.raw('''SELECT id, ip, count(*) from apache_log_log
                                GROUP BY id, ip
                                ORDER BY count(*) ASC LIMIT 10;''')[:10]
    data['most_common_ips'] = list(map(lambda l: l.ip, list(most_common_ips)))
    return JsonResponse(data)


def download_logs(request):
    logs = search(request.GET)
    labels = ['ip', 'date', 'http_method',
              'uri', 'status_code', 'response_size']
    wb = Workbook() # Make xlsx workbook
    ws = wb.active # get active page of workbook. Default first page
    ws.title = 'logs' # make title of page
    ws.append(labels) # put labels
    for l in logs:
        l_dict = model_to_dict(l)
        ws.append([l_dict[label] for label in labels]) # put line of log
    response = HttpResponse(save_virtual_workbook(
        wb), content_type="application/vnd.ms-excel") # save to memory and send
    response['Content-Disposition'] = 'inline; filename=apache_log.xlsx'
    return response
