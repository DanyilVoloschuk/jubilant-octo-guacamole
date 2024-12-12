from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = self.queryset

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user',
                openapi.IN_QUERY,
                description="specify user by id",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="specify start date",
                type=openapi.FORMAT_DATETIME,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="specify end date",
                type=openapi.FORMAT_DATETIME,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user',
                openapi.IN_QUERY,
                description="specify user by id",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "month",
                openapi.IN_QUERY,
                description="specify month",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def category_summary(self, request):
        user_id = request.query_params.get('user')
        month = request.query_params.get('month')
        if not (user_id and month):
            return Response({"error": "User ID and month are required"}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(user_id=user_id, date__month=month)
        summary = expenses.values('category').annotate(total=Sum('amount'))
        return Response(summary)
