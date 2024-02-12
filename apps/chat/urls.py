from django.urls import path
from .views import MyInbox, GetMessages, SendMessages, SearchUser
app_name = 'apps.chat'
urlpatterns = [
    path('my-messages/<int:user_id>/', MyInbox.as_view(), name='my-inbox'),
    path('get-messages/<int:sender_id>/<int:receiver_id>/', GetMessages.as_view(), name='get-messages'),
    path('send-messages/', SendMessages.as_view(), name='send-messages'),
    path("search/<username>/", SearchUser.as_view(), name='search'),
]