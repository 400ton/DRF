from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_price, create_stripe_session


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.payment_sum)
        session_id, payment_link = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
