from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from utils.serializer_validator import validate_serializer


class AddRevenueExpenditureApi(APIView):
    permission_classes = [ExpertPermission, ]

    class RequestSerializer(serializers.Serializer):
        revenue = serializers.FloatField(required=False)
        expenditure = serializers.FloatField(required=False)
        year = serializers.IntegerField(required=True)
        month = serializers.IntegerField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = RevenueExpenditure
            fields = '__all__'

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        creator = request.user
        organization = creator.client
        revenue_expenditure = add_revenue_expenditure(data=request_serializer.validated_data, creator=creator, organization=organization)
        response_serializer = self.ResponseSerializer(revenue_expenditure)
        return Response({
            'revenue_expenditure': response_serializer.data
        }, status=status.HTTP_200_OK)

class UpdateRevenueExpenditureApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        revenue = serializers.FloatField(required=False)
        expenditure = serializers.FloatField(required=False)      

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = RevenueExpenditure
            fields = '__all__'

    def put(self, request, revenue_expenditure_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        revenue_expenditure = get_revenue_expenditure_by(raise_exception=False, id=revenue_expenditure_id).first()
        self.check_object_permissions(request=request, obj=revenue_expenditure)
        revenue_expenditure = update_revenue_expenditure(revenue_expenditure=revenue_expenditure, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(revenue_expenditure)
        return Response({
            'revenue_expenditure': response_serializer.data
        }, statu=status.HTTP_200_OK)

class DeleteRevenueExpenditureApi(APIView):
    permission_classes = [OwnerPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = RevenueExpenditure
            fields = '__all__'

    def delete(self, request, revenue_expenditure_id):
        revenue_expenditure = get_revenue_expenditure_by(raise_exception=False,id=revenue_expenditure_id).first()
        self.check_object_permissions(request=request, obj=revenue_expenditure)
        revenue_expenditure = delete_revenue_expenditure(revenue_expenditure)
        response_serializer = self.ResponseSerializer(revenue_expenditure)
        return Response({
            'revenue_expenditure': response_serializer.data
        }, status=status.HTTP_200_OK)
    
class RevenueExpenditureListApi(APIView):
    permission_classes = [IsAuthenticated, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = RevenueExpenditure
            fields = '__all__'

    def get(self, request, start, end):
        start_year = int(str(start)[0:4])
        start_month = int(str(start)[4:])
        end_year = int(str(end)[0:4])
        end_month = int(str(end)[4:])
        user = request.user
        revenue_expenditures = list(get_revenue_expenditure_by(organization=user.client, month__lte=end_month, month__gte=start_month, year__lte=end_year, year__gte=start_year))
        response_serializer = self.ResponseSerializer(revenue_expenditures, many=True)
        return Response({
            'revenue_expenditures': response_serializer.data
        }, status=status.HTTP_200_OK)

        
    