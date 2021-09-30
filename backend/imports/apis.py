from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer
from .models import Import


class AddImportApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        _import = serializers.FloatField(required=False)
        domestic_economy = serializers.FloatField(required=False)
        foreign_invested_economy = serializers.FloatField(required=False)
        machinery_equipment = serializers.FloatField(required=False)
        plastic_material = serializers.FloatField(required=False)
        cashew = serializers.FloatField(required=False)
        rubber = serializers.FloatField(required=False)
        cloth =  serializers.FloatField(required=False)
        iron_steel = serializers.FloatField(required=False)
        animal_feed = serializers.FloatField(required=False)
        chemical = serializers.FloatField(required=False)
        textile_material = serializers.FloatField(required=False)
        metal = serializers.FloatField(required=False)
        corn = serializers.FloatField(required=False)
        chemical_product = serializers.FloatField(required=False)
        textile_yarn = serializers.FloatField(required=False)
        electronic_product = serializers.FloatField(required=False)
        cotton = serializers.FloatField(required=False)
        pesticide = serializers.FloatField(required=False)
        wood_product = serializers.FloatField(required=False)
        medicine = serializers.FloatField(required=False)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Import
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        _import = add_import(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(_import)
        return Response({
            'import': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateImportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        _import = serializers.FloatField(required=False)
        domestic_economy = serializers.FloatField(required=False)
        foreign_invested_economy = serializers.FloatField(required=False)
        machinery_equipment = serializers.FloatField(required=False)
        plastic_material = serializers.FloatField(required=False)
        cashew = serializers.FloatField(required=False)
        rubber = serializers.FloatField(required=False)
        cloth =  serializers.FloatField(required=False)
        iron_steel = serializers.FloatField(required=False)
        animal_feed = serializers.FloatField(required=False)
        chemical = serializers.FloatField(required=False)
        textile_material = serializers.FloatField(required=False)
        metal = serializers.FloatField(required=False)
        corn = serializers.FloatField(required=False)
        chemical_product = serializers.FloatField(required=False)
        textile_yarn = serializers.FloatField(required=False)
        electronic_product = serializers.FloatField(required=False)
        cotton = serializers.FloatField(required=False)
        pesticide = serializers.FloatField(required=False)
        wood_product = serializers.FloatField(required=False)
        medicine = serializers.FloatField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Import
            fields = '__all__'

    def put(self, request, import_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        _import = get_import_by(raise_exception=False, id=import_id).first()
        self.check_object_permissions(request=request, obj=_import)
        _import = update_import(_import=_import, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(_import)
        return Response({
            'import': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteImportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Import
            fields = '__all__'

    def delete(self, request, import_id):
        _import = get_import_by(raise_exception=False,id=import_id).first()
        self.check_object_permissions(request=request, obj=_import)
        _import = delete_import(_import)
        response_serializer = self.ResponseSerializer(_import)
        return Response({
            'import': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class ImportListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Import
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        imports = list(Import.objects.filter(organization=user.client, month__gte=start_month, year=start_year) | Import.objects.filter(organization=user.client, year__gte=start_year, year__lte=end_year) | Import.objects.filter(organization=user.client, month__lte=end_month, year=end_year))              

        response_serializer = self.ResponseSerializer(imports, many=True)
        return Response({
            'imports': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    