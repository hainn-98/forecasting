from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer
from .models import Iip


class AddIipApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        IIP = serializers.FloatField(required=False)
        mining_industry = serializers.FloatField(required=False)
        manufacturing_processing_industry = serializers.FloatField(required=False)
        gas_electricity_industry = serializers.FloatField(required=False)
        waste_treatment_water_supply = serializers.FloatField(required=False)
        mineral_exploitation = serializers.FloatField(required=False)
        food = serializers.FloatField(required=False)
        cigarette = serializers.FloatField(required=False)
        textile = serializers.FloatField(required=False)
        costume = serializers.FloatField(required=False)
        leather_product = serializers.FloatField(required=False)
        paper_product = serializers.FloatField(required=False)
        chemical_product = serializers.FloatField(required=False)
        plastic_product = serializers.FloatField(required=False)
        non_metalic_mineral_product = serializers.FloatField(required=False)
        prefabricated_metal_product = serializers.FloatField(required=False)
        electrical_product = serializers.FloatField(required=False)
        motor_vehicle = serializers.FloatField(required=False)
        furniture = serializers.FloatField(required=False)
        other_manufacturing_processing = serializers.FloatField(required=False)
        water_supply = serializers.FloatField(required=False)
        gas_electricity = serializers.FloatField(required=False)
        other_products = serializers.FloatField(required=False)       
        base_period = serializers.CharField(max_length=50, required=True)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Iip
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        iip = add_iip(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(iip)
        return Response({
            'iip': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateIipApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        IIP = serializers.FloatField(required=False)
        mining_industry = serializers.FloatField(required=False)
        manufacturing_processing_industry = serializers.FloatField(required=False)
        gas_electricity_industry = serializers.FloatField(required=False)
        waste_treatment_water_supply = serializers.FloatField(required=False)
        mineral_exploitation = serializers.FloatField(required=False)
        food = serializers.FloatField(required=False)
        cigarette = serializers.FloatField(required=False)
        textile = serializers.FloatField(required=False)
        costume = serializers.FloatField(required=False)
        leather_product = serializers.FloatField(required=False)
        paper_product = serializers.FloatField(required=False)
        chemical_product = serializers.FloatField(required=False)
        plastic_product = serializers.FloatField(required=False)
        non_metalic_mineral_product = serializers.FloatField(required=False)
        prefabricated_metal_product = serializers.FloatField(required=False)
        electrical_product = serializers.FloatField(required=False)
        motor_vehicle = serializers.FloatField(required=False)
        furniture = serializers.FloatField(required=False)
        other_manufacturing_processing = serializers.FloatField(required=False)
        water_supply = serializers.FloatField(required=False)
        gas_electricity = serializers.FloatField(required=False)
        other_products = serializers.FloatField(required=False)       
        base_period = serializers.CharField(max_length=50, required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Iip
            fields = '__all__'

    def put(self, request, iip_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        iip = get_iip_by(raise_exception=False, id=iip_id).first()
        self.check_object_permissions(request=request, obj=iip)
        iip = update_iip(iip=iip, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(iip)
        return Response({
            'iip': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteIipApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Iip
            fields = '__all__'

    def delete(self, request, iip_id):
        iip = get_iip_by(raise_exception=False,id=iip_id).first()
        self.check_object_permissions(request=request, obj=iip)
        iip = delete_iip(iip)
        response_serializer = self.ResponseSerializer(iip)
        return Response({
            'iip': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class IipListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Iip
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        if start_year != end_year:
            iips = set(Iip.objects.filter(organization=user.client, month__gte=start_month, year=start_year) | Iip.objects.filter(organization=user.client, year__gt=start_year, year__lt=end_year) | Iip.objects.filter(organization=user.client, month__lte=end_month, year=end_year))              
        else:
            iips = set(Iip.objects.filter(organization=user.client, month__gte=start_month, month__lte=end_month, year=start_year))
        response_serializer = self.ResponseSerializer(iips, many=True)
        return Response({
            'iips': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    