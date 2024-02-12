from rest_framework import serializers
from .models import ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']  
        ref_name = 'ChatUserSerializer'  

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'is_read', 'date']
        read_only_fields = ['id', 'date', 'is_read'] 

    def create(self, validated_data):

        user = self.context['request'].user
        receiver = validated_data['receiver']  
        message = ChatMessage.objects.create(
            sender=user,
            receiver=receiver,
            message=validated_data['message']
        )
        return message