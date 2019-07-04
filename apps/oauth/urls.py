from . import views
from django.conf.urls import url

urlpatterns = [
    url("^login/$", views.LoginView.as_view(), name="login"),
    url("^sign_up/$", views.RegisterView.as_view(), name="signup"),
    url("^logout/$", views.logout_action, name="logout"),
    url("^api/user/get/all", views.get_all_user_info, name="get_all"),
    url("^api/user/get/developer", views.get_all_develop_info, name="get_developer"),
    url("^api/user/get/(?P<id>[0-9]+)/$", views.get_user_by_id, name="get_user"),
    url("^api/user/update/(?P<id>[0-9]+)/$", views.update_user_by_id, name="update_user"),
    url("^api/user/delete/(?P<id>[0-9]+)/$", views.delete_user_by_id, name="delete_user"),
    url("^main/", views.get_main, name='main'),
    url("^test/", views.test, name="test"),

    #path("test1/", views.test1view.as_view(),name="test1")
    #path("register/", views.register),

    #path("SignUP/re")
]
