from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer
from .models import Export


class AddExportApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        export = serializers.FloatField(required=False)
        domestic_economy = serializers.FloatField(required=False)
        foreign_invested_economy = serializers.FloatField(required=False)
        footwear = serializers.FloatField(required=False)
        textile_product = serializers.FloatField(required=False)
        textile_yarn = serializers.FloatField(required=False)
        wood_product = serializers.FloatField(required=False)
        machinery_equipment = serializers.FloatField(required=False)
        transport_vehicle = serializers.FloatField(required=False)
        coffe = serializers.FloatField(required=False)
        iron_steel_product = serializers.FloatField(required=False)
        electronic_product = serializers.FloatField(required=False)
        cashew = serializers.FloatField(required=False)
        plastic_product = serializers.FloatField(required=False)
        pepper = serializers.FloatField(required=False)
        rubber = serializers.FloatField(required=True)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Export
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        export = add_export(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(export)
        return Response({
            'export': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateExportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        export = serializers.FloatField(required=False)
        domestic_economy = serializers.FloatField(required=False)
        foreign_invested_economy = serializers.FloatField(required=False)
        footwear = serializers.FloatField(required=False)
        textile_product = serializers.FloatField(required=False)
        textile_yarn = serializers.FloatField(required=False)
        wood_product = serializers.FloatField(required=False)
        machinery_equipment = serializers.FloatField(required=False)
        transport_vehicle = serializers.FloatField(required=False)
        coffe = serializers.FloatField(required=False)
        iron_steel_product = serializers.FloatField(required=False)
        electronic_product = serializers.FloatField(required=False)
        cashew = serializers.FloatField(required=False)
        plastic_product = serializers.FloatField(required=False)
        pepper = serializers.FloatField(required=False)
        rubber = serializers.FloatField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Export
            fields = '__all__'

    def put(self, request, export_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        export = get_export_by(raise_exception=False, id=export_id).first()
        self.check_object_permissions(request=request, obj=export)
        export = update_export(export=export, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(export)
        return Response({
            'export': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteExportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Export
            fields = '__all__'

    def delete(self, request, export_id):
        export = get_export_by(raise_exception=False,id=export_id).first()
        self.check_object_permissions(request=request, obj=export)
        export = delete_export(export)
        response_serializer = self.ResponseSerializer(export)
        return Response({
            'export': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class ExportListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Export
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        exports = list(Export.objects.filter(organization=user.client, month__gte=start_month, year=start_year) | Export.objects.filter(organization=user.client, year__gte=start_year, year__lte=end_year) | Export.objects.filter(organization=user.client, month__lte=end_month, year=end_year))              

        response_serializer = self.ResponseSerializer(exports, many=True)
        return Response({
            'exports': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    