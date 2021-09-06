from django.db import models
from django.utils.translation import ungettext
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Unemployment
from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer
import logging

class AddUnemploymentApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        rate = serializers.FloatField(required=False)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Unemployment
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
       
        unemployment = add_unemployment(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(unemployment)
        return Response({
            'unemployment': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateUnemploymentApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        rate = serializers.FloatField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Unemployment
            fields = '__all__'

    def put(self, request, unemployment_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        unemployment = get_unemployment_by(raise_exception=False, id=unemployment_id).first()
        self.check_object_permissions(request=request, obj=unemployment)
        unemployment = update_unemployment(unemployment, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(unemployment)
        return Response({
            'unemployment': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteUnemploymentApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Unemployment
            fields = '__all__'

    def delete(self, request, unemployment_id):
        unemployment = get_unemployment_by(raise_exception=False,id=unemployment_id).first()
        self.check_object_permissions(request=request, obj=unemployment)
        unemployment = delete_unemployment(unemployment)
        response_serializer = self.ResponseSerializer(unemployment)
        return Response({
            'unemployment': response_serializer.data
        }, status=status.HTTP_200_OK)
    
# class UnemploymentListApi(APIView):
#     permission_classes = [IsAuthenticated, ]

#     class ResponseSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Unemployment
#             fields = '__all__'

#     def get(self, request):
#         user = request.user
#         unemployments = list(get_unemployment_by(organization=user.client, month=12))
#         response_serializer = self.ResponseSerializer(unemployments, many=True)
#         return Response({
#             'unemployments': response_serializer.data
#         }, status=status.HTTP_200_OK)

class UnemploymentListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Unemployment
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        unemployments = set(list(get_unemployment_by(organization=user.client, month__gte=start_month, year=start_year)) + \
                list(get_unemployment_by(organization=user.client, year__gte=start_year, year__lte=end_year)) + \
                list(get_unemployment_by(organization=user.client, month__lte=end_month, year=end_year)))
        
        response_serializer = self.ResponseSerializer(unemployments, many=True)
        return Response({
            'unemployments': response_serializer.data
        }, status=status.HTTP_200_OK)