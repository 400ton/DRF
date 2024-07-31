from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserUpdate, UserList, UserCreate, PaymentsList, UserDelete, PaymentsCreate

app_name = UsersConfig.name

urlpatterns = [
    path('', UserList.as_view(), name='users_list'),
    path('update/<int:pk>', UserUpdate.as_view(), name='user_update'),
    path('register/', UserCreate.as_view(), name='user_register'),
    path('delete/<int:pk>', UserDelete.as_view(), name='user_delete'),
    path('payments/', PaymentsList.as_view(), name='payments_list'),
    # path('payments-pay/', PaymentsCreate.as_view(), name='payments_pay'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
