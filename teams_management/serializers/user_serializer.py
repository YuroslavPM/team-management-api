from rest_framework import serializers
from django.contrib.auth.models import User
from teams_management.models.user_profile import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(write_only = False)
    lastName = serializers.CharField(write_only = False)
    email = serializers.EmailField(write_only = False)

    secret = serializers.CharField(write_only= False)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'displayName', 'email', 'firstName', 
            'lastName', 'secret', 'createdAt', 'updatedAt', 'isAdmin'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('secret')
        first_name = validated_data.pop('firstName')
        last_name = validated_data.pop('lastName')

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
            **validated_data
        )
        return profile
    

    def update(self, instance, validated_data):
        user = instance.user

        if 'email' in validated_data:
            user.email = validated_data.pop('email')
            user.username = user.email

        if 'fistName' in validated_data:
            user.first_name = validated_data.pop('firstName')
        
        if 'lastName' in validated_data:
            user.last_name = validated_data.pop('lastName')

        if 'secret' in validated_data:
            password = validated_data.pop('secret')
            user.set_password(password)
            instance.secret = password

        user.save()

        return super().update(instance, validated_data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['firstName'] = instance.user.first_name
        representation['lastName'] = instance.user.last_name
        representation['email'] = instance.user.email

        return representation