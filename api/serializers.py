from rest_framework import serializers

class UserCheckSerializer(serializers.Serializer):
    tg_login = serializers.CharField(max_length=32)

class TelegramMessageSerializer(serializers.Serializer):
    # tg_login = serializers.CharField(max_length=32)
    user_text = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        help_text='Email, phone number, or Telegram ID'
    )
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    tg_login = serializers.CharField(max_length=32)
    password = serializers.CharField(write_only=True, min_length=8)
