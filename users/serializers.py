from rest_framework import serializers

from users.models import CustomUser, Payments, PaymentLinkModel


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLinkModel
        fields = "__all__"
