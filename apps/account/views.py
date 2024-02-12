
from http import HTTPStatus
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LogOutSerializer, UserProfileSerializer, UserGetProductSerializer, UserVipGetSerializer
from django.contrib.auth import get_user_model
from .send_email import send_confirmation_email
from django.shortcuts import get_object_or_404
from .tasks import send_confirm_email_task, send_password_reset_task, send_vip_email_task
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser 
from rest_framework import generics, viewsets
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_confirm_email_task.delay(user.email, user.activation_code[0:7])
            except:
                return Response(
                    {
                        'message': 'Че то не то, на почте нет ниче',
                        'data': serializer.data
                    }, status=HTTPStatus.CREATED
                )
            return Response(serializer.data, status=HTTPStatus.CREATED)
    

class ActivationView(APIView):
    def post(self, request):
        code = request.data.get('activation_code')
        user = User.objects.filter(activation_code__startswith=code[:6]).first()
        if user:
            user.is_active = True
            user.activation_code = ''
            user.save()
            try:
                return Response({
                    'message': 'Пользователь активирован',
                    'email': user.email  # Добавим email пользователя в ответ
                }, status=HTTPStatus.OK)
            except Exception as e:
                return Response(
                    {'error': f'Ошибка при отправке подтверждения по электронной почте: {e}'},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {'error': 'Пользователь с указанным кодом активации не найден.'},
                status=HTTPStatus.NOT_FOUND
            )
        

class LogoutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        # Проверяем, был ли предоставлен refresh token
        if refresh_token:
            # Если предоставлен, то добавляем его в черный список
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('Успешно разлогинились', status=200)
        else:
            # Если refresh token не был предоставлен, возвращаем ошибку
            return Response('Отсутствует refresh token', status=400)


class CustomResetPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        email = request.user.email
        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'ValidationError': 'Нет такого пользователя'}, 400)
        
        user_id = user.id
        send_password_reset_task.delay(email=email, user_id=user_id)
        return Response('Вам на почту отправили сообщение', status=200)
    
    def post(self, request, *args, **kwargs):
        new_password = request.data.get('new_password')
        password_confirm = request.data.get('password_confirm')
        user_id = kwargs.get('uidb64') 
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response('Пользователь не найден', status=404)

        if not new_password or not password_confirm:
            return Response('Пожалуйста, укажите новый пароль и подтверждение пароля', status=400)

        if new_password != password_confirm:
            return Response('Пароли не совпадают', status=400)
        try:
            validate_password(new_password, user=user)
        except Exception as e:
            return Response(str(e), status=400)
        user.set_password(new_password)
        user.save()
        return Response('Ваш пароль изменен!', status=201)    

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

class UserDetailView(generics.RetrieveAPIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.last_online = timezone.now()
        serializer = UserProfileSerializer(user)
        user.save()
        return Response(serializer.data)

    
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

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request):
        user = request.user
        user.delete()
        return Response('Вы удалили аккаунт', status=HTTPStatus.OK)
    

class ChangeClosedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        if user.is_closed:
            user.is_closed = False
            user.save()
            return Response('Вы открыли доступ к аккаунту', status=HTTPStatus.OK)
        else:
            user.is_closed = True
            user.save()
            return Response('Вы закрыли доступ к аккаунту', status=HTTPStatus.OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    serializer_class = UserGetProductSerializer

        
class UserVipGetViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    serializer_class = UserVipGetSerializer

class IsOnlineView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        is_online = user.is_online()
        online_info = user.get_online_info()
        
        user.last_online = timezone.now()
        user.save()

        return Response({'is_online': is_online, 'online_info': online_info}, status=HTTPStatus.OK)
        