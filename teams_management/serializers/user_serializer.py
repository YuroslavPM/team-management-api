from rest_framework import serializers
from django.contrib.auth.models import User
from teams_management.models.user_profile import UserProfile


class UserProfileReadSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'display_name', 'email', 'first_name',
            'last_name', 'created_at', 'updated_at', 'is_admin'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserProfileWriteSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    secret = serializers.CharField(write_only=True)  

    class Meta:
        model = UserProfile
        fields = [
            'id', 'display_name', 'email', 'first_name',
            'last_name', 'secret', 'created_at', 'updated_at', 'is_admin'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('secret')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name', f"{first_name} {last_name}".strip())

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return UserProfile.objects.create(
            user=user,
            display_name=display_name,
            **validated_data
        )

    def update(self, instance, validated_data):
        user = instance.user

        if 'email' in validated_data:
            user.email = validated_data.pop('email')
            user.username = user.email

        if 'first_name' in validated_data:  
            user.first_name = validated_data.pop('first_name')

        if 'last_name' in validated_data:
            user.last_name = validated_data.pop('last_name')

        if 'secret' in validated_data:
            user.set_password(validated_data.pop('secret'))

        user.save()
        return super().update(instance, validated_data)