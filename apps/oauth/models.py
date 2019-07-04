from django.db import models
from django.contrib.auth.models import AbstractUser

from tools.utils import sha_256
# Create your models here.


class User(AbstractUser):
    ROLE_ITEMS = [
        (0, ("管理员")),
        (1, ("开发者")),
        (2, ("普通用户"))
    ]

    uid = models.AutoField(db_column='uid', verbose_name='用户编号',max_length=10,primary_key=True, null=False ,unique=True)
    username = models.CharField(db_column='username', verbose_name='用户名', max_length=150, null=False, blank=False, unique=True)
    password = models.CharField(db_column='password',  verbose_name='密码', max_length=150, null=False, blank=False)
    name = models.CharField(db_column='name', verbose_name='姓名', max_length=150, null=True, blank=True)
    is_active = models.BooleanField(db_column='is_active', verbose_name='用户状态',default=True)
    role = models.PositiveIntegerField(db_column="role", verbose_name='用户角色', choices=ROLE_ITEMS, default=2)

    class Meta:
        verbose_name = '用户信息'
        db_table = "User"

    # @classmethod
    # def reset_password(cls, password):
    #     cls.password = sha_256(password)
    #     return True
    #
    # @classmethod
    # def vaild_user(cls, username, password):
    #     user = cls.objects.get(username=username)
    #     return user.username == username and user.password == password and user.is_active is True
    #
    # @classmethod
    # def delete_user(cls):
    #     cls.is_active = False
    #     return True
    #
    # @classmethod
    # def become_admin(cls):
    #     cls.role = 0
    #
    # @classmethod
    # def become_developer(cls):
    #     cls.role = 1

class GroupUser(models.Model):
    uid = models.IntegerField(db_column="uid", verbose_name='用户编号', null=False, blank=False)
    gid = models.IntegerField(db_column="gid", verbose_name='组编号' ,null=False,blank=False)

    class Meta:
        verbose_name = '用户、组关系表'
        db_table = "GroupUser"

class Group(models.Model):
    gid = models.AutoField(db_column='gid', verbose_name='组编号', primary_key=True, blank=False, null=False)
    update = models.BooleanField(db_column="update", verbose_name='修改字段', default=False)

    class Meta:
        verbose_name = '组信息表'
        db_table = "Group"




    # @classmethod
    # def get_all_group(self):
    #     return self.objects.all().values_list("gname")
    #

