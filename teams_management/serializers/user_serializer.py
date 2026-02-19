from rest_framework import serializers
from django.contrib.auth.models import User
from teams_management.models.user_profile import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only = True)
    last_name = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    secret = serializers.CharField(write_only= False)
    display_name = serializers.CharField(required = False)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'display_name', 'email', 'first_name', 
            'last_name', 'secret', 'created_at', 'updated_at', 'is_admin'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('secret')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        display_name = validated_data.pop('display_name', f"{first_name} {last_name}".strip())

        user = User.objects.create_user(
            username=email,
            email=email,
            password = password,
            first_name = first_name,
            last_name = last_name
        )

        profile = UserProfile.objects.create(
            user= user,
            secret = password,
            display_name = display_name,
            **validated_data
        )
        return profile
    

    def update(self, instance, validated_data):
        user = instance.user

        if 'email' in validated_data:
            user.email = validated_data.pop('email')
            user.username = user.email

        if 'fist_name' in validated_data:
            user.first_name = validated_data.pop('first_name')
        
        if 'last_name' in validated_data:
            user.last_name = validated_data.pop('last_name')

        if 'secret' in validated_data:
            password = validated_data.pop('secret')
            user.set_password(password)
            instance.secret = password

        user.save()

        return super().update(instance, validated_data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['email'] = instance.user.email

        return representation