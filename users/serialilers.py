from rest_framework.serializers import CharField, ModelSerializer

from users.models import Payment, User
from users.validators import CourseOrLessonValidator


class PaymentSerializer(ModelSerializer):
    method = CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "date",
        ]

    validators = [
        CourseOrLessonValidator(),
    ]


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "avatar", "city")


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "phone", "city", "avatar")


class UserUpdateSerializer(ModelSerializer):
    password = CharField(style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("email", "password", "phone", "city", "avatar")

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(validated_data.get("password", instance.password))
        instance.phone = validated_data.get("phone", instance.phone)
        instance.city = validated_data.get("city", instance.city)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance
