from django.urls import path
from . import views


app_name='oaauth'


urlpatterns=[
    path('login', views.LoginView.as_view(), name='login'),
    path('imgCheck', views.ImgCheckView.as_view(), name='imgCheck'),
    path('resetpwd', views.ResetPwdView.as_view(), name='resetpwd')
]