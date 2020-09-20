'''
Written by Andrew Perera
Copyright 2020
'''

from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from users.models import UserAccount

UserAccount = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, validated_data):
        user = None

        email = validated_data.get('email')
        password = validated_data.get('password')

        if email and password:
            user = authenticate(self.context['request'], email=email, password=password)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
            user.update_last_login()
        else:
            msg = _("We couldn't log you in with provided credentials.")
            raise exceptions.ValidationError(msg)

        return user

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ['key']
