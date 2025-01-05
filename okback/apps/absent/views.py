from django.shortcuts import render
from django.template.defaulttags import querystring
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class AbsentViewSet(viewsets.ModelViewSet):
    queryset = Absent.objects.all()
    serializer_class =AbsentSerializer

    # put()
    def update(self, request, *args, **kwargs):
        # 默认情况下，如果要修改某一条数据，那么要把这个数据的序列化中指定的字段都上传
        # 如果想只修改一部分数据，那么可以在kwargs中设置partial为True
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    #get()
    def list(self,request,*args,**kwargs):
        queryset=Absent.objects.all()
        who=request.query_params.get('who')
        if who and who=='sub':
            result=queryset.filter(responder=request.user)
        else :
            result=queryset.filter(requester=request.user)

        #分页
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response：除了返回序列化后的数据外，还会返回总数据多少，上一页url是什么
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(result, many=True)
        return Response(data=serializer.data)


#请假类型列表
class AbsentTypeView(APIView):
    def get(self,request):
        queryset = AbsentType.objects.all()
        return Response(data=AbsentTypeSerializer(queryset,many=True).data)

#显示审批者
class ResponderView(APIView):
    def get(self,request):
        user=request.user
        if user.department.leader.uid==user.uid:#是部门领导
            if user.department.name=='董事会':
                responder=None
            else:
                responder=user.department.manager
        else:
            responder = user.department.leader
        return Response(data=UserSerializer(responder).data)





