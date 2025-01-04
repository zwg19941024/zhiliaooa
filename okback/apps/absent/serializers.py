
from rest_framework import serializers
from .models import *
from apps.oaauth.serializers import UserSerializer


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only=True)#只在ORM序列化成字典时用到，write_only=True只在校验时用到
    absent_type_id = serializers.IntegerField(write_only=True)#只会字典序列化ORM时用到，返回数据给前端时无这个
    requester = UserSerializer(read_only=True)
    responder = UserSerializer(read_only=True)
    class Meta:
        model = Absent
        fields = '__all__'
    #验证type是否存在
    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise serializers.ValidationError('不存在的请假类型')
        return value

    def create(self, validated_data):
        request=self.context['request']
        user=request.user#在token里有user记录
        if user.department.leader.uid==user.uid:#是部门领导
            if user.department.name=='董事会':
                responder=None
                validated_data['status']=AbsentStatusChoices.PASS
            else:
                responder=user.department.manager
        else:
            responder = user.department.leader
        requester = user
        return Absent.objects.create(requester=requester, responder=responder,**validated_data)

    #审批者处理考勤
    def update(self, instance, validated_data):#instance已经给你找到Absent对象了
        if instance.status!=AbsentStatusChoices.AUDITING:
            raise serializers.ValidationError(detail='审核中的请假单才能修改')

        request = self.context.get('request')  # 会有问题，我前端没有传对象过去
        user = request.user
        if instance.responder!=user:#审批者能看到别人的审批的请假单么
            raise serializers.ValidationError(detail='您无权处理该考勤')

        instance.status=validated_data.get('status')
        instance.response_content=validated_data.get('response_content')
        instance.save()
        return instance





