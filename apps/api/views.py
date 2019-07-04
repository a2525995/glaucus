from django.shortcuts import render
from tools.json_response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from apps.oauth.models import Group, GroupUser
from apps.oauth.serializers import GroupSerializer
from apps.api.serializers import ProjectSerializer
import logging

# Create your views here.

log = logging.getLogger(__file__)

@login_required
def dashboard(request):
    return render(request, "main/project.html")

#@login_required
@api_view(['POST'])
def create_project(request, id):
    """
    :param request:
    :param id: user_id
    :return:
    """
    result = {
        "data": None,
        "msg": "success",
        "code": 200
    }
    owner_id = id
    receive_data = JSONParser().parse(request)
    developer = receive_data.pop("developer")

    if not developer:
        result['msg'] = "failed"
        result['code'] = 1001
        return JsonResponse(data=result['data'], code=result['code'], msg=result['msg'])

    for k in list(receive_data.keys()):
        if receive_data.get(k) is None:
            receive_data.pop(k)
    group_data = dict(create_or_delete=False, update=True)
    #创建组
    group = GroupSerializer(data=group_data)

    if not group.is_valid():
        result['msg'] = "failed"
        result['code'] = 1002
        return JsonResponse(data=result['data'], code=result['code'], msg=result['msg'])

    g = group.save()
    receive_data.update({'owner_id': owner_id})
    #建立每个用户和组之间的关系
    for user_id in developer:
        GroupUser.objects.create(uid=user_id, gid=g.gid)
    p = ProjectSerializer(data=receive_data)
    if not p.is_valid():
        result['msg'] = "failed"
        result['code'] = 1003
        return JsonResponse(data=result['data'], code=result['code'], msg=result['msg'])
    project = p.save()
    data = ProjectSerializer(instance=project).data
    #建立项目和组的关系
    ProjectGroup.objects.create(pid=project.pid, gid=g.gid)
    data.update(dict(developer=developer))
    return JsonResponse(data=data, code=200, msg="success")

@login_required
@require_http_methods(['POST'])
def update_project(request):
    pid = request.POST.get('project_id')
    group_user = set()
    group_project = set()
    try:
        for group in GroupUser.objects.filter(uid=request.user.uid):
            group_user.add(group.gid)
        for group in ProjectGroup.objects.filter(pid=pid):
            group_project.add(group.gid)
        group = group_user.intersection(group_project)
    except TypeError:
        group = None

    if not group:
        return None

    for id in group:
        g = Group.objects.get(gid=id)
        if g.update:
            pname = request.POST.get('project_name')
            description = request.POST.get('description')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            deadline = request.POST.get('deadline')
            p = Project.objects.get(pid=pid)
            p.pname = pname
            p.description = description
            p.start_time = start_time
            p.end_time = end_time
            p.deadline = deadline
            p.save()
            return JsonResponse({"msg": "success"})
    #TODO(owner才能更新组)

    return JsonResponse({"msg": "user not authorized"})

@api_view(['GET'])
def get_all_project_by_id(request, id):
    l = list()
    try:
        gids = GroupUser.objects.filter(uid=id).values_list('gid', flat=True)
        pids = ProjectGroup.objects.filter(gid__in=gids).values_list("pid", flat=True)
        for pid in pids:
            l.append(ProjectSerializer(instance=Project.objects.filter(pid=pid).first()).data)
    except Exception as e:
        log.info(e)
    return JsonResponse(data=l, msg="success", code=200)

@api_view(['GET'])
def get_project_by_pid(request, id):
    result = {
        "data": None,
        "code": 200,
        "msg": "success"
    }
    d = {}
    try:
        p = Project.objects.filter(pid=id).first()
        data = ProjectSerializer(instance=p).data
        gids = ProjectGroup.objects.filter(pid=id).values_list('gid', flat=True)
        developer = GroupUser.objects.filter(gid__in=gids).values_list('uid', flat=True)
        d.update(data)
        d.update({"developer": developer})
    except Exception as e:
        log.info(e)
    return JsonResponse(data=d, msg=result['msg'], code=result['code'])




    # try:
    #     gid_list = GroupUser.objects.filter(uid=request.user.uid).values_list("gid", flat=True)
    #     pid_list = ProjectGroup.objects.filter(gid__in=gid_list).values_list("pid", flat=True)
    #     project = Project.objects.filter(Q(pid__in=pid_list) | Q(is_public=True)).values_list("pid", "pname", "description", "owner_id", "start_time", "end_time", "deadline")
    #
    #     print(project)
    #
    # except TypeError:
    #     pass
    #
    # return JsonResponse({"msg": "success"})






# def accept_message(request):
#     data = {
#         "msg": "ok",
#         "result": "1"
#     }
#     log.info("123")
#     return JsonResponse(data, status=200)
#
# #
# def get_model(request):
#     #obj = UserInfo.objects.all().values()
#     obj = []
#     print(obj)
#     obj = list(obj)
#     print(type(obj[1]))
#     d = {
#         "test": obj
#     }
#     return JsonResponse(data=d, safe=False)
#

