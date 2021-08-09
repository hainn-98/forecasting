import re
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from users.permissions import *
from .services import *
from .models import User
from utils.serializer_validator import validate_serializer


class SignInApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        auth_token = authenticate_user(**request_serializer.validated_data)
        user = auth_token.user
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data,
            'token': auth_token.key
        }, status=status.HTTP_200_OK)

class UserUpdateApi(APIView):
    permission_classes = [UserPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
    
    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        user = get_user_by(id=request.user.id)
        self.check_object_permissions(request=request, obj=user)
        user = update_user(data=request_serializer.validated_data, user=user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)

class UserDetailApi(APIView):
    permission_classes=[UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']
        
    def get(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        })

class UserDeactivateApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']
    
    def delete(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = deactivate_user(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)

class UserActivateApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']

    def put(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = activate(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)

class UserChangePasswordApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)
        password_confirmation = serializers.CharField(required=True, max_length=255)

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        user = get_user_by(id=request.user.id)
        self.check_object_permissions(request=request, obj=user)
        change_password(user=user, data=request_serializer.validated_data)
        return Response({

        }, status=status.HTTP_200_OK)

class UserRequestResetPasswordApi(APIView):
    permission_classes=[AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        generate_password_token(data=request_serializer.validated_data)
        return Response({

        }, status=status.HTTP_200_OK)

class UserResetPasswordApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        reset_password_token = serializers.CharField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)
        password_confirmation = serializers.CharField(required=True, max_length=255)

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        reset_password(data=request_serializer.validated_data)
        return Response({

        }, status=status.HTTP_200_OK)

class UserSignOutApi(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request):
        expire_token(request.user)
        return Response({

        }, status=status.HTTP_200_OK)



class UserCreateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(required=True, max_length=255)
        email = serializers.CharField(required=True, max_length=255)
        role = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'role', 'change_init_password',
                      'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        client = request.user.client
        user, _ = create_user(data=request_serializer.validated_data, client=client)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
