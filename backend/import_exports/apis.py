from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer


class AddImportExportApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        _import = serializers.FloatField(required=False)
        export = serializers.FloatField(required=False)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ImportExport
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        import_export = add_import_export(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(import_export)
        return Response({
            'import_export': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateImportExportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        _import = serializers.FloatField(required=False)
        export = serializers.FloatField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ImportExport
            fields = '__all__'

    def put(self, request, import_export_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        import_export = get_import_export_by(raise_exception=False, id=import_export_id).first()
        self.check_object_permissions(request=request, obj=import_export)
        import_export = update_import_export(import_export=import_export, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(import_export)
        return Response({
            'import_export': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteImportExportApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ImportExport
            fields = '__all__'

    def delete(self, request, import_export_id):
        import_export = get_import_export_by(raise_exception=False,id=import_export_id).first()
        self.check_object_permissions(request=request, obj=import_export)
        import_export = delete_import_export(import_export)
        response_serializer = self.ResponseSerializer(import_export)
        return Response({
            'import_export': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class ImportExportListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = ImportExport
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        import_exports = list(get_import_export_by(organization=user.client, month__lte=end_month, month__gte=start_month, year__lte=end_year, year__gte=start_year))
        response_serializer = self.ResponseSerializer(import_exports, many=True)
        return Response({
            'import_exports': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    