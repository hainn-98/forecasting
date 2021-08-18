from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer


class AddCpiApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        CPI = serializers.FloatField(required=False)
        food_service = serializers.FloatField(required=False)
        eating_out = serializers.FloatField(required=False)
        cereal = serializers.FloatField(required=False)
        food = serializers.FloatField(required=False)
        beverage_cigarette = serializers.FloatField(required=False)
        garment = serializers.FloatField(required=False)
        household_equipment = serializers.FloatField(required=False)
        housing = serializers.FloatField(required=False)
        medicine_medical_service = serializers.FloatField(required=False)
        communication = serializers.FloatField(required=False)
        telecommunication = serializers.FloatField(required=False)
        education = serializers.FloatField(required=False)
        culture_entertainment_travel = serializers.FloatField(required=False)
        other_good_services = serializers.FloatField(required=False)
        base_period = serializers.CharField(max_length=50, required=False)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)


    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cpi
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        cpi = add_cpi(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(cpi)
        return Response({
            'cpi': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateCpiApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        CPI = serializers.FloatField(required=False)
        food_service = serializers.FloatField(required=False)
        eating_out = serializers.FloatField(required=False)
        cereal = serializers.FloatField(required=False)
        food = serializers.FloatField(required=False)
        beverage_cigarette = serializers.FloatField(required=False)
        garment = serializers.FloatField(required=False)
        household_equipment = serializers.FloatField(required=False)
        housing = serializers.FloatField(required=False)
        medicine_medical_service = serializers.FloatField(required=False)
        communication = serializers.FloatField(required=False)
        telecommunication = serializers.FloatField(required=False)
        education = serializers.FloatField(required=False)
        culture_entertainment_travel = serializers.FloatField(required=False)
        other_good_services = serializers.FloatField(required=False)
        base_period = serializers.CharField(max_length=50, required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cpi
            fields = '__all__'

    def put(self, request, cpi_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        cpi = get_cpi_by(raise_exception=False, id=cpi_id).first()
        self.check_object_permissions(request=request, obj=cpi)
        cpi = update_cpi(cpi=cpi, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(cpi)
        return Response({
            'cpi': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteCpiApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cpi
            fields = '__all__'

    def delete(self, request, cpi_id):
        cpi = get_cpi_by(raise_exception=False,id=cpi_id).first()
        self.check_object_permissions(request=request, obj=cpi)
        cpi = delete_cpi(cpi)
        response_serializer = self.ResponseSerializer(cpi)
        return Response({
            'cpi': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class CpiListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Cpi
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        cpis = list(get_cpi_by(organization=user.client, month__lte=end_month, month__gte=start_month, year__lte=end_year, year__gte=start_year))
        response_serializer = self.ResponseSerializer(cpis, many=True)
        return Response({
            'cpis': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    