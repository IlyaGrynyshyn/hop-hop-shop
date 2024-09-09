from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone

from rest_framework import serializers

from authentication.models import PasswordReset
from authentication.utils import send_reset_password_email


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class CustomerSerializer(serializers.ModelSerializer):
    user_role = serializers.SerializerMethodField()

    def get_user_role(self, obj) -> str:
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
            "avatar",
            "phone_number",
            "shipping_country",
            "shipping_city",
            "shipping_address",
            "shipping_postcode",
            "user_role",
        )
        read_only_fields = ["id", "user_role"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def validate(self, attrs):
        attrs = super().validate(attrs)
        filtered_attrs = {
            k: v for k, v in attrs.items()
            if not isinstance(v, str) or (isinstance(v, str) and v != "")
        }

        return filtered_attrs

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


class CustomerAdminSerializer(CustomerSerializer):
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
            "avatar",
            "shipping_country",
            "shipping_city",
            "shipping_address",
            "shipping_postcode",
            "is_staff",
            "user_role",
            "is_active",
        )
        read_only_fields = ["id", "password"]

    def update(self, instance, validated_data):
        """Update a user, set the role or deactivate their account"""
        is_staff = validated_data.pop("is_staff", None)
        is_active = validated_data.pop("is_active", None)
        validated_data.pop("password", None)

        user = super().update(instance, validated_data)

        if is_staff is not None:
            user.is_staff = is_staff
        if is_active is not None:
            user.is_active = is_active

        user.save()

        return user


class ResetPasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = PasswordReset
        fields = ('email',)

    def validate(self, attrs):
        user = get_user_model().objects.filter(email__iexact=attrs["email"]).first()
        if not user:
            raise serializers.ValidationError("There is no user with provided email")

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        attrs['token'] = token
        attrs['user_id'] = user.id

        return attrs

    def create(self, validated_data):
        token = validated_data.pop('token', None)
        email = validated_data.pop('email', None)
        user_id = validated_data.pop('user_id', None)

        reset_password = PasswordReset.objects.filter(user_id=user_id).first()

        if reset_password:
            reset_password.delete()

        instance = PasswordReset(user_id=user_id, token=token)
        instance.save()

        send_reset_password_email(user_id, token, email)

        return instance


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
    user_id = serializers.IntegerField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """
        Validate the password reset token, expiration, and password match.
        :param attrs:
        :return:
        """
        user = get_user_model().objects.filter(id=attrs['user_id']).first()
        if not user:
            raise serializers.ValidationError("There is no user with the provided id.")

        reset_password = PasswordReset.objects.filter(user_id=user.id).first()
        if not reset_password:
            raise serializers.ValidationError("Wrong recovery address, provided user didn't request "
                                              "recovery password.")

        valid_token = reset_password.token == attrs["token"]
        is_expired = reset_password.expires_at < timezone.now()

        if is_expired:
            raise serializers.ValidationError("The provided token is expired.")

        if not valid_token:
            raise serializers.ValidationError("Invalid secret token value.")

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def save(self, **kwargs):
        user = get_user_model().objects.filter(id=self.validated_data["user_id"]).first()
        user.set_password(self.validated_data["password"])
        user.save()

        reset_password = PasswordReset.objects.filter(user_id=self.validated_data["user_id"]).first()
        reset_password.delete()


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
