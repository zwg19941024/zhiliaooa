from rest_framework import serializers
from apps.oaauth.models import UserStatusChoices, OAUser, OADepartment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "请输入邮箱！"})
    password = serializers.CharField(max_length=20, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("请输入正确的邮箱！")
            if not user.check_password(password):
                raise serializers.ValidationError("请输入正确的密码！")
            # 判断状态
            if user.status == UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError("该用户尚未激活！")
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError("该用户已被锁定，请联系管理员！")
            # 为了节省执行SQL语句的次数，这里我们把user直接放到attrs中，方便在视图中使用
            attrs['user'] = user
        else:
            raise serializers.ValidationError('请传入邮箱和密码！')
        return attrs


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = OAUser
        exclude = ('password', 'groups','user_permissions')

class ResetPwdSerializer(serializers.Serializer):
    uid = serializers.CharField()
    oldpwd = serializers.CharField(max_length=20, min_length=6)
    newpwd1 = serializers.CharField(max_length=20, min_length=6)
    newpwd2 = serializers.CharField(max_length=20, min_length=6)
    def validate(self, attrs):
        uid = attrs['uid']
        oldpwd=attrs['oldpwd']
        newpwd1=attrs['newpwd1']
        newpwd2=attrs['newpwd2']
        OAUser_object = OAUser.objects.get(uid=uid)
        if not OAUser_object.check_password(oldpwd):
            raise serializers.ValidationError("旧密码错误")
        if newpwd1 != newpwd2:
            raise serializers.ValidationError("新密码不一样")
        OAUser_object.set_password(newpwd1)
        OAUser_object.save()
        return attrs