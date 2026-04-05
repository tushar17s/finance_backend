from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import FinancialRecord, AppUser
from .serializers import FinancialRecordSerializer, RegisterUserSerializer
from django.db.models.functions import TruncMonth, TruncWeek
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

#  Helper: Get user safely
def get_user_from_request(request):
    if not request.user or not request.user.is_authenticated:
        return None, Response({"error": "Authentication required"}, status=401)

    try:
        app_user = request.user.appuser   

        if not app_user.is_active:
            return None, Response({"error": "User inactive"}, status=403)

        return app_user, None

    except AppUser.DoesNotExist:
        return None, Response({"error": "AppUser not found"}, status=404)

#  Permission check
def check_permission(user, method, endpoint):

    # VIEWER -> only dashboard APIs
    if user.role == 'VIEWER':
        if endpoint in ['summary', 'category_summary', 'recent'] and method == 'GET':
            return True
        return False

    #  ANALYST -> read-only access
    if user.role == 'ANALYST':
        if method in ['POST', 'PUT', 'DELETE']:
            return False
        return True

    # ADMIN -> full access
    return True


#  CREATE + LIST RECORDS
@api_view(['GET', 'POST'])
def record_list_create(request):
    user, error = get_user_from_request(request)
    if error:
        return error

    # GET records
    if request.method == 'GET':
        if not check_permission(user, request.method, 'records'):
            return Response({"error": "Permission denied"}, status=403)

        #  Admin + Analyst -> all records
        if user.role in ['ADMIN', 'ANALYST']:
            records = FinancialRecord.objects.all()
        else:
            records = FinancialRecord.objects.none()

        # Filtering 
        category = request.query_params.get('category')
        record_type = request.query_params.get('type')

        if category:
            records = records.filter(category=category.upper())

        if record_type:
            records = records.filter(type=record_type.upper())

        serializer = FinancialRecordSerializer(records, many=True)
        return Response(serializer.data)

    # POST record
    elif request.method == 'POST':
        if not check_permission(user, request.method, 'records'):
            return Response({"error": "Permission denied"}, status=403)

        serializer = FinancialRecordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# GET SINGLE + UPDATE + DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def record_detail(request, pk):
    user, error = get_user_from_request(request)
    if error:
        return error

    try:
        record = FinancialRecord.objects.get(pk=pk)
    except FinancialRecord.DoesNotExist:
        return Response({"error": "Record not found"}, status=404)

    # GET single
    if request.method == 'GET':
        if not check_permission(user, request.method, 'record_detail'):
            return Response({"error": "Permission denied"}, status=403)

        serializer = FinancialRecordSerializer(record)
        return Response(serializer.data)

    # UPDATE
    elif request.method == 'PUT':
        if not check_permission(user, request.method, 'record_detail'):
            return Response({"error": "Permission denied"}, status=403)

        serializer = FinancialRecordSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE
    elif request.method == 'DELETE':
        if not check_permission(user, request.method, 'record_detail'):
            return Response({"error": "Permission denied"}, status=403)

        record.delete()
        return Response(status=204)


#  REGISTER USER


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'VIEWER').upper()

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username exists"}, status=400)

    #  create auth user
    user = User.objects.create(
        username=username,
        password=make_password(password)
    )

    # create AppUser
    AppUser.objects.create(user=user, role=role)

    return Response({"message": "User registered"}, status=201)

@api_view(['GET'])
def dashboard(request):
    user, error = get_user_from_request(request)
    if error:
        return error

    if not check_permission(user, request.method, 'summary'):
        return Response({"error": "Permission denied"}, status=403)

    # SUMMARY
    income = FinancialRecord.objects.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense = FinancialRecord.objects.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

    summary_data = {
        "total_income": income,
        "total_expense": expense,
        "net_balance": income - expense
    }

    #  CATEGORY SUMMARY
    category_data = FinancialRecord.objects.values('category').annotate(total=Sum('amount')).order_by('-total')

    #  RECENT TRANSACTIONS
    if user.role == 'ADMIN' or user.role == 'ANALYST':
        recent_records = FinancialRecord.objects.order_by('-date')[:5]
    else :
        recent_records = FinancialRecord.objects.none()
    recent_serializer = FinancialRecordSerializer(recent_records, many=True)

    #  FINAL RESPONSE
    return Response({
        "summary": summary_data,
        "category_summary": category_data,
        "recent_transactions": recent_serializer.data
    })


@api_view(['GET'])
def trends(request):
    user, error = get_user_from_request(request)
    if error:
        return error

    #  Permission 
    if not check_permission(user, request.method, 'trend'):
        return Response({"error": "Permission denied"}, status=403)

    #  Get query param (monthly or weekly)
    trend_type = request.query_params.get('type', 'monthly')

    if trend_type == 'weekly':
        data = FinancialRecord.objects.annotate(
            period=TruncWeek('date')
        ).values('period', 'type').annotate(
            total=Sum('amount')
        ).order_by('period')

    else:  # default monthly
        data = FinancialRecord.objects.annotate(
            period=TruncMonth('date')
        ).values('period', 'type').annotate(
            total=Sum('amount')
        ).order_by('period')

    return Response({
        "trend_type": trend_type,
        "data": data
    })