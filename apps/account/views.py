
from http import HTTPStatus

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LogOutSerialzer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .send_email import send_confirmation_email
from django.shortcuts import get_object_or_404
from .tasks import send_confirm_email_task, send_password_reset_task, send_vip_email_task
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser 
from rest_framework import generics

User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirm_email_task.delay(user.email, user.activation_code)
            except:
                return Response(
                    {
                        'message': 'Че то не то, на почте нет ниче',
                        'data': serializer.data
                    }, status=HTTPStatus.CREATED
                )
            return Response(serializer.data, status=HTTPStatus.CREATED)
    

class ActivationView(APIView):
    def get(self, request):
        code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        try:
            send_confirmation_email(user.email, user.activation_code)
            return Response({
                'message': 'Пользователь активирован'}, status=HTTPStatus.OK
            )
        except Exception as e:
            return Response(
                {'error': f'Ошибка при отправке подтверждения по электронной почте: {e}'},
                            status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        

class LogoutView(APIView):
    serializer_class = LogOutSerialzer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно разлогинилсь', 200)


class CustomResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        user_id = user.id
        if not user:
            return Response({'ValidationError': 'Нет такого пользователя'}, status=HTTPStatus.BAD_REQUEST)
        
        send_password_reset_task.delay(email=email, user_id=user_id)
        return Response('Вам на почту отправили сообщение', 200)
    

class CustomPasswordConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        new_password = request.data.get('new_password')
        password_confirm = request.data.get('password_confirm')
        user_id = self.kwargs.get('uidb64')
        user = User.objects.get(id=user_id)
        if new_password != password_confirm:
            return Response('Пароли не совпадают', 404)
        user.set_password(new_password)
        user.save()
        return Response('', 201)
        

class VipView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.is_staff == False:
            user.is_staff = True
            user.save()
            send_vip_email_task.delay(user.email, user.username)
            return Response('Вы стали vip пользователем', status=HTTPStatus.OK)
        else:
            return Response('Вы уже vip', status=HTTPStatus.BAD_REQUEST)


class UserProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    
class UsernameUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        new_username = request.data.get('username')

        if not user.can_change_username():
            return Response({'detail': 'ты можешь менять своё имя только раз в месяц'}, status=400)

        user.update_username(new_username)
        return Response({'detail': 'Username updated successfully.'})

