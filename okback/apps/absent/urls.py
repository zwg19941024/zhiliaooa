from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


app_name='absent'

router=DefaultRouter(trailing_slash=False)
#absent/absent
router.register('absent', views.AbsentViewSet,basename='absent')

urlpatterns=[
    #absent/absentType
    path('absentType', views.AbsentTypeView.as_view(), name='absentType'),
    path('responder', views.ResponderView.as_view(), name='responder')
            ]+router.urls