from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from .models import ChatMessage
from .serializers import MessageSerializer
from rest_framework.response import Response
from apps.account.models import CustomUser
from apps.account.serializers import UserProfileSerializer

class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id  
        return ChatMessage.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id)).distinct().order_by('-date')
    
class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        user = self.request.user

        if user.id not in [sender_id, receiver_id]:
            raise PermissionDenied("You do not have permission to view these messages.")
        
        return ChatMessage.objects.filter(
            Q(sender_id=sender_id, receiver_id=receiver_id) |
            Q(sender_id=receiver_id, receiver_id=sender_id)
        ).distinct().order_by('-date')
    
class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class SearchUser(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = CustomUser.objects.filter(Q(username__icontains=username) | Q(user__email__icontains=username))

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)