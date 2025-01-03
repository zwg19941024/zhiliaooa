from django.db import models

from apps.oaauth.models import OAUser


class AbsentStatusChoices(models.IntegerChoices):
    # 进行中
    AUDITING = 1
    # 通过
    PASS = 2
    # 拒绝
    REJECT = 3


class AbsentType(models.Model):
    name = models.CharField(max_length=100)
    creata_time = models.DateTimeField(auto_now_add=True)


class Absent(models.Model):
    #标题
    title = models.CharField(max_length=200)
    # 内容
    request_content=models.TextField()
    # 类型
    absent_type = models.ForeignKey(AbsentType, on_delete=models.CASCADE,related_name='absents',related_query_name='absents')
    # 发起人
    requester=models.ForeignKey(OAUser,on_delete=models.CASCADE,related_name='req_absents',related_query_name='req_absents')
    # 审批人
    responder=models.ForeignKey(OAUser,on_delete=models.CASCADE,related_name='resp_absents',related_query_name='resp_absents',null=True)
    # 状态
    status=models.IntegerField(choices=AbsentStatusChoices,default=AbsentStatusChoices.AUDITING)
    # 开始时间
    start_date=models.DateField()
    # 结束时间
    end_date=models.DateField()
    # 发起时间
    create_time=models.DateTimeField(auto_now_add=True)
    # 回复
    response_content=models.TextField()



