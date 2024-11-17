import time
from http.client import HTTPResponse

from django.http import HttpRequest
from django.shortcuts import render
from django.utils.cache import get_conditional_response


def setup_useragent_on_request_middleware(get_response):

    print('initial call')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print('after get response')
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.request_time = {}
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        # time_delay = 10
        # if not self.request_time:
        #     print('Это первый request после перезапуска сервера, словарь еще пуст!!')
        # else:
        #     if (round(time.time()) * 1) - self.request_time['time'] < time_delay \
        #        and self.request_time['ip_address'] == request.META.get('REMOTE_ADDR'):
        #         print('Прошло меньше 10 секунд для повторного запроса с вашего ip-адреса!')
        #         return render(request, 'requestdataapp/error-request.html')

        # self.request_time = {'time': round(time.time()) * 1, 'ip_address': request.META.get('REMOTE_ADDR')}
        self.requests_count += 1
        print('requests count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response


    def process_exception(self, requests:HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exeptions so far")
