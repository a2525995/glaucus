from . import views
from django.urls import path
from django.conf.urls import url

urlpatterns = [

    #path("main/", views.get_index, name="main"),
    path("main/dashboard", views.dashboard, name="dashboard"),
    url(r"project/create/(?P<id>[0-9]+)/$", views.create_project, name="create_project"),
    path("update_project", views.update_project, name="update_project"),
    url(r"project/get/all/(?P<id>[0-9]+)/$", views.get_all_project_by_id, name="get_project"),
    url(r"project/get/(?P<id>[0-9]+)/$", views.get_project_by_pid, name="get_project_by_pid"),
    #path("SignUP/re")
]
