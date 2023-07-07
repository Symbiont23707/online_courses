from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
import logging

from .models import User
from .serializers import UserSerializer
from ..students.serializers import StudentSerializer
from ..teachers.serializers import TeacherSerializer


# Create your views here.
class RegisterView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        role = request.data.get('role')
        specialty = request.data.get('specialty')

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if role == 'Student':
            student_data = {'user': user.uuid, 'specialty': specialty}
            serializer_student = StudentSerializer(data=student_data)
            serializer_student.is_valid(raise_exception=True)
            serializer_student.save()
        else:
            teacher_data = {'user': user.uuid}
            serializer_teacher = TeacherSerializer(data=teacher_data)
            serializer_teacher.is_valid(raise_exception=True)
            serializer_teacher.save()

        return Response(serializer.data)

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#         user = User.objects.filter(username=username).first()
#
#         if User is None:
#             raise AuthenticationFailed('User not found!')
#
#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')
#
#         payload = {
#             'uuid': str(user.uuid),
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }
#
#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#
#         response = Response()
#
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#         return response

# class UserView(APIView):
#
#     def get(self, request):
#         token = request.COOKIES.get('jwt')
#
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')
#
#         user = User.objects.filter(uuid=payload['uuid']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
