import re

import requests
from django.core.management.base import BaseCommand
from test_task.settings import DEBUG

from apache_log.models import Log
from datetime import datetime

class Command(BaseCommand):
    help = 'Load Apache log.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Link to Apache log file')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        print(f'Start load log from {url}', flush=True)
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise Exception(f'Failed on request. Status code: {response.status_code}')
        total_len = int(response.headers['content-length'])
        dl = 0
        num_lines = 0
        last_line = ''
        for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                lines = data.decode('utf-8').split('\n')
                if len(lines) == 1:
                    last_line += lines[0]
                    continue
                first_line,*lines,last_line_t = lines
                lines = [last_line+first_line] + lines
                last_line = last_line_t

                logs_objects = []
                for line in lines:
                    if line:
                        r = re.match(r'([(\d\.)]+) - - \[(.*?)\] "(\w+) (.*) .*" (\d+) ([0-9\-]*)',line)
                        if not r:
                            continue
                        log_dict = dict(zip(['ip','date','http_method','uri','status_code','response_size'],r.groups()))
                        log_dict['date'] = datetime.strptime(log_dict['date'], '%d/%b/%Y:%H:%M:%S %z')
                        log_dict['response_size'] = 0 if log_dict['response_size'] == '-' else int(log_dict['response_size'])
                        log_object = Log(**log_dict)
                        logs_objects += [log_object]
                num_lines += len(lines)
                Log.objects.bulk_create(logs_objects)
                if DEBUG and num_lines > 400:
                    break
                done = 100 * dl / total_len
                print(f'[{"=" * int(done/2)}{" " * int(50-done/2)}] {done: .2f}%                 \n\033[F', flush=True, end='')    
        print(f'\nDone. Loaded {num_lines} lines of log', flush=True)