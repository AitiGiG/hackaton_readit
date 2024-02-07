from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm','username'
        ]

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class LogOutSerialzer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'biography', 'avatar', 'link', 'is_closed', 'is_staff']