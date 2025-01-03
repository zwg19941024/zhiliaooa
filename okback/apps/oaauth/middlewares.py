from asyncio import exceptions

import jwt
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError
from rest_framework.authentication import get_authorization_header

from apps.oaauth.models import OAUser
from okback import settings


class LoginCheckMiddleware(MiddlewareMixin):
    keyword = 'JWT'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.white_list=['/auth/login','/auth/register']

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.white_list:
            request.user=AnonymousUser()
            request.auth=None
            return None
        try:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.AuthenticationFailed('请传入JWT！')

            if len(auth) == 1:
                msg = "不可用的JWT请求头！"
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = '不可用的JWT请求头！JWT Token中间不应该有空格！'
                raise exceptions.AuthenticationFailed(msg)

            try:
                jwt_token = auth[1]
                jwt_info = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms='HS256')
                userid = jwt_info.get('userid')
                try:
                    # 绑定当前user到request对象上
                    user = OAUser.objects.get(pk=userid)
                    request.user = user
                    request.auth=jwt_token
                except:
                    msg = '用户不存在！'
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = "JWT Token已过期！"
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            return JsonResponse({'detail': '请先登录'}, status=400)
