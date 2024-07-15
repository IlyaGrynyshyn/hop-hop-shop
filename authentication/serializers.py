from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def validate(self, data):
        """
        Check that the password and confirm_password match.
        """
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "Password and confirm password do not match."
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_staff": user.is_staff,
        }

        data.update({"user": user_data})

        return data
