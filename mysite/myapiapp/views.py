from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from django.contrib.auth.models import Group
from .serializers import GroupSerializers

@api_view()
def api_hello_view(request: Request) -> Response:
    return Response({"message": "Hello!"})


# class GroupsListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         # data = [group.name for group in groups] - без использования serialize
#         serialized = GroupSerializers(groups, many=True)
#         return Response({"groups": serialized.data})

# ListModelMixin
# class GroupsListView(ListModelMixin ,GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializers
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)

# ListCreateAPIView
class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers
