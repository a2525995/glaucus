# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    pid = models.AutoField(db_column="pid", primary_key=True, null=False ,unique=True)
    pname = models.CharField(db_column="pname", max_length=150, null=False, blank=False)
    description = models.CharField(db_column="description", max_length=255)
    owner_id = models.IntegerField(db_column="owner_id", null=False, blank=False)
    start_time = models.DateField(db_column="start_time", default=None, null=True, blank=True)
    end_time = models.DateField(db_column="end_time", default=None, null=True, blank=True)
    deadline = models.DateField(db_column="deadline", default=None, null=True, blank=True)
    is_public = models.BooleanField(db_column="is_public", default=False)
    #TODO(koushushin):增加api

class ProjectGroup(models.Model):
    pid = models.IntegerField(db_column="pid", null=False, blank=False)
    gid = models.IntegerField(db_column="gid", null=False, blank=False)

class Story(models.Model):
    PRIORITY_LEVEL = [1, 2, 3, 4, 5]
    sid = models.AutoField(db_column='sid', primary_key=True, blank=False, null=False)
    sname = models.CharField(db_column='sname', max_length=150, null=False, blank=False)
    description = models.CharField(db_column="description", max_length=255)
    api_id = models.IntegerField(db_column="api_id", default=None)
    priority = models.IntegerField(db_column="priority", default=5)
    value = models.IntegerField(db_column="value", default=None)
    create_time = models.DateTimeField(db_column="create_time", auto_now_add=True)
    update_time = models.DateTimeField(db_column="update_time", auto_now=True)
    status = models.CharField(db_column="status", max_length=30)

