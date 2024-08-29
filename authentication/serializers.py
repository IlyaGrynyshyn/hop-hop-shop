from django.contrib.auth import get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CustomerSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()

    def get_user_role(self, obj):
        if obj.is_superuser:
            return "Admin"
        elif obj.is_staff:
            return "Staff"
        return "User"

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "user_role",
        )
        read_only_fields = ["id", "user_role"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CustomerAdminSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "is_staff",
            "is_active",
        )
        read_only_fields = ["id", "password"]

    def update(self, instance, validated_data):
        """Update a user, set the role or deactivate their account"""
        is_staff = validated_data.pop("is_staff", None)
        is_active = validated_data.pop("is_active", None)

        user = super().update(instance, validated_data)

        if is_staff is not None:
            user.is_staff = is_staff
        if is_active is not None:
            user.is_active = is_active

        user.save()

        return user



class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        """
        Validate that the password and password2 match
        :param attrs:
        :return:
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def validate_old_password(self, value):
        """
        Validate old password against current password
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        """
        Update user password with new password
        """
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
