from apps.oauth.models import User
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from tools.utils import sha_256, get_current
from tools.redis_service import RedisService
from glaucus.settings import TOKEN_EXPIRE_TIME

import logging

logger = logging.getLogger(__name__)


def generator_token(user_id):
    '''根据user_id生成token'''
    token = sha_256(str(user_id) + str(get_current()))
    RedisService.set_key(token, user_id, TOKEN_EXPIRE_TIME)
    return token


def get_all_user():
    """获取所有用户信息"""
    return User.objects.all()


def get_user_info_by_id(filter_type, keywords):
    """根据基本信息查找用户"""
    user = None
    if filter_type == 'id':
        try:
            user = User.objects.get(id=keywords)
        except ObjectDoesNotExist as e:
            logger.error(e)
    elif filter_type == 'username':
        try:
            user = User.objects.get(username=keywords)
        except ObjectDoesNotExist as e:
            logger.error(e)
    return user

def get_group_by_userid(user_id):
    """获取user_id对应所有的group"""

def get_project_by_userid(user_id):
    """获取user_id对应所有的project信息"""
    sql = f"select api_project.* from " \
          f"(select pid from (SELECT gid FROM `oauth_groupuser` where uid = {user_id})a" \
          f" left join api_projectgroup on a.gid = api_projectgroup.gid " \
          f"where pid > 0)b left join api_project on b.pid = api_project.pid"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        projects = cursor.fetchall()
        if projects is not None and len(projects) > 0:
            for _project in projects:
                ''
    return res



if __name__ == '__main__':
    print(generator_token(1))
