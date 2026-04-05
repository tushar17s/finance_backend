from rest_framework import serializers
from .models import AppUser, FinancialRecord   

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser   
        fields = ['id', 'username', 'role']

    def validate_username(self, value):
        if AppUser.objects.filter(username=value).exists():   
            raise serializers.ValidationError("Username already exists")
        return value
    

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = AppUser
        fields = ['id', 'username', 'role']


class FinancialRecordSerializer(serializers.ModelSerializer):
    
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FinancialRecord
        fields = [
            'id',
            'amount',
            'type',
            'category',
            'date',
            'notes',
            'created_by'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def validate_type(self, value):
        if value not in ['INCOME', 'EXPENSE']:
            raise serializers.ValidationError("Type must be INCOME or EXPENSE")
        return value
    
    def validate_category(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category cannot be empty")
        return value

    def validate_notes(self, value):
        if value and len(value) > 200:
            raise serializers.ValidationError("Notes too long (max 200 chars)")
        return value