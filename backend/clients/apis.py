from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import User
from .services import *
from .models import Client
from .permissions import *
from utils.serializer_validator import validate_serializer


class SignUpApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.CharField(required=True, max_length=255)
        client_name = serializers.CharField(required=True, max_length=255)
        address = serializers.CharField(required=True, max_length=255)
        name = serializers.CharField(required=True, max_length=255)
    
    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'address', 'is_active', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        client = create_client(data=request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)

class ClientDetailApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'address', 'is_active', 'created_at', 'updated_at']

    def get(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)

class ClientUpdateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        client_name = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'address', 'is_active', 'created_at', 'updated_at']

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        client = get_client_by(id=request.user.client.id)
        self.check_object_permissions(request=request, obj=client)
        client = update_client(client=client, data=request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientDeactivateApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'address', 'is_active', 'created_at', 'updated_at']

    def delete(self, request):
        client = get_client_by(id=request.user.client.id)
        self.check_object_permissions(request=request, obj=client)
        client = deactivate_client(client=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientActivateApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'address', 'is_active', 'created_at', 'updated_at']

    def put(self, request):
        client = get_client_by(only_deleted=False, id=request.user.client.id)
        self.check_object_permissions(request=request, obj=client)
        client = activate_client(client=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientListUsersApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email',  'role', 'created_at', 'updated_at']

    def get(self, request):
        client = get_client_by(id=request.user.client.id)
        self.check_object_permissions(request=request, obj=client)
        users = list(client.users.all())
        response_serializer = self.ResponseSerializer(users, many=True)
        return Response({
            'users': response_serializer.data
        }, status=status.HTTP_200_OK)
