# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.urls import reverse
from tools.utils import *
from .models import User, GroupUser
import json
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import UserSerializer
from tools.json_response import RestJsonResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from apps.oauth.service import generator_token
from tools.redis_service import RedisService
from glaucus.settings import TOKEN_EXPIRE_TIME
import logging
from django.db.models import Q
from django.views.generic import TemplateView

# Create your views here.

logger = logging.getLogger(__file__)


class LoginView(APIView):
    def get(self, request):
        return render(request, 'account/index.html')

    def post(self, request):
        result = {
            "data": None,
            "msg": "success",
            "code": 200
        }
        receive_data = json.loads(request.body)
        username = receive_data['username']
        password = receive_data['password']

        if not all([username, password]):
            result['msg'] = '必须填入全部信息'
            result['code'] = 500

            return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'],
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        password = sha_256(password)
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        if not user or user.is_active is False:
            result['msg'] = '用户名密码不正确'
            result['code'] = 500

            return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'],
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        res = user.vaild_user(username, password)
        if res:
            login(request, user)
            generator_token(user.uid)
            RedisService.set_key(generator_token(user.uid), user.uid, TOKEN_EXPIRE_TIME)

            return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'])
        # 用户名 密码不正确
        result['msg'] = '用户名密码不正确'
        result['code'] = 500
        return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'],
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterView(APIView):
    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):
        logger.info("begin to register user")
        result = {
            'code': 200,
            'msg': "success",
            "data": None
        }
        receive_data = json.loads(request.body)
        username = receive_data['username']
        password = receive_data['password']
        if not all([username, password]):
            result['msg'] = '必须填入全部信息'
            result['code'] = 400
            return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'],
                                status=status.HTTP_400_BAD_REQUEST)

        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        if user:
            result['msg'] = '该用户名已经被注册'
            result['code'] = 400
            return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'],
                                status=status.HTTP_400_BAD_REQUEST)

        password = sha_256(password)

        user = User.objects.create(username=username, password=password, name=username)
        user.save()
        return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'])


@require_http_methods(['POST'])
def find_back(request):
    result = {
        "data": None,
        "code": 200,
        "msg": "success"
    }
    username = request.POST.get("form-username")
    user = None
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        pass
    if not user or not user.is_active:
        return RestJsonResponse(data=result['data'], code=result['code'], msg=result['msg'])

    # TODO(koushushin): send email


@api_view(['GET'])
@login_required
def logout_action(request):
    try:
        logout(request)
    except Exception:
        pass
    return RestJsonResponse(data=None, code=200, msg="success")


@api_view(['GET'])
def get_all_user_info(request):
    user = User.objects.all()
    serialize = UserSerializer(user, many=True)
    return RestJsonResponse(data=serialize.data, code=200, msg="success")


@api_view(['GET'])
def get_all_develop_info(request):
    user = User.objects.filter(Q(admin=True) | Q(developer=True))
    serialize = UserSerializer(user, many=True)
    return RestJsonResponse(data=serialize.data, code=200, msg="success")


@api_view(['GET'])
def get_user_by_id(request, id):
    user = User.objects.filter(uid=id).first()
    if not user:
        return RestJsonResponse(data=None, code=400, msg="user not in system")
    serialize = UserSerializer(user)
    return RestJsonResponse(data=serialize.data, code=200, msg="success")


@api_view(['POST'])
def update_user_by_id(request, id):
    user = User.objects.filter(uid=id).first()
    if not user:
        return RestJsonResponse(data=None, code=400, msg="user not in system")
    receive_data = JSONParser().parse(request)
    serializer = UserSerializer(instance=user)
    serializer.update(instance=user, validated_data=receive_data)
    return RestJsonResponse(data=serializer.data, code=200, msg="success")


@api_view(['GET'])
def delete_user_by_id(request, id):
    user = User.objects.filter(uid=id).first()
    if not user:
        return RestJsonResponse(data=None, code=400, msg="user not in system")
    user.is_active = False
    user.save()
    return RestJsonResponse(data=None, code=200, msg="success")


def get_main(request):
    return render(request, 'main/first_page.html')

def test(request):
    from .service import get_project_by_userid
    data = get_project_by_userid(1)
    return JsonResponse({"data": data})

# class test1view(APIView):
#     def get(self, request):
#         data = {
#             'username': "test12345677@163.com",
#             'password': "123",
#             'name': "123",
#             "is_active": True,
#             "admin": False,
#             "developer": False,
#         }
#         user = UserSerializer(data=data)
#         res = user.is_valid()
#         print(res)
#         print(user.errors)
#         user.save()
#         return RestJsonResponse(user.data, code=200, msg="success")
