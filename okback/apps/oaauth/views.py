from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.oaauth.authentications import generate_jwt
from io import BytesIO

from apps.oaauth.models import OAUser
from apps.oaauth.serializers import LoginSerializer, UserSerializer, ResetPwdSerializer
from pillow.pillow import myImgCode
import hashlib


# Create your views here.

class ImgCheckView(APIView):
    def get(self, request):
        imgCode=myImgCode()
        img,code_str=imgCode.createImg()

        #1. 验证码写入session里.可以has加密
        md = hashlib.md5(code_str.encode())
        request.session['image_code']=md
        request.session.set_expiry(60)

        # 3. 写入内存(Python3)
        stream = BytesIO()
        img.save(stream, 'png')
        return Response(stream.getvalue())



class LoginView(APIView):
    def post(self, request):
        # 1. 验证数据是否可用
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            user.last_login=datetime.now()
            user.save()
            token=generate_jwt(user)
            return Response({'token':token,'user':UserSerializer(user).data},status=status.HTTP_200_OK)
        else:
            return Response({'detail':list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)

class ResetPwdView(APIView):
    def post(self, request):
        serializer = ResetPwdSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response({'detail':list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)
