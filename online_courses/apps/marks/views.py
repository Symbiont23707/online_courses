from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps import marks
from apps.marks.models import Mark, Comment
from apps.marks.serializers import MarkSerializer, CommentSerializer

# from apps.marks.serializers import MarkSerializer, CommentSerializer
from apps.users.models import Student

class MarkAPIView(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

class MarkDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    lookup_field = 'uuid'

class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# class MarkViewSet(viewsets.ModelViewSet):
#     queryset = Mark.objects.all()
#     serializer_class = MarkSerializer

# class Comments(APIView):
#
#     def get(self, request):
#
#         mark = request.data["mark"]
#         if Comment.objects.filter(mark=mark).exists():
#
#             mark = Comment.objects.get(mark=mark)
#             return Response({
#                 'Home_task': mark.comment,
#             })
#         else:
#             return Response("Comment doesn't exists", status=status.HTTP_400_BAD_REQUEST)
#     def post(self, request):
#         serializer = CommentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data)

# class MyMarks(APIView):
#
#     def get(self, request):
#         student = Student.objects.get(user=request.user.uuid)
#         completed_homeworks = student.home_task_set.all()
#         serializer = MarkSerializer(marks, many=True)
#         return Response(serializer.data)

