from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

# function -> change the way data is represented

UserAccount = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # define input fields
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50, allow_blank=True)
    last_name = serializers.CharField(max_length=50, allow_blank=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = UserAccount
        # return fields
        fields = ['id', 'email', 'first_name', 'last_name',
                  'password', 'confirm_password', 'date_joined']

    def validate(self, validated_data):
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if password != confirm_password:
            raise exceptions.ValidationError(_("Your passwords must match."))

        return validated_data

    def get_cleaned_data(self, validated_data):
        return {
            "email": validated_data.get("email"),
            "first_name": validated_data.get("first_name"),
            "last_name": validated_data.get("last_name"),
            "password": validated_data.get("password")
        }

    def create(self, validated_data):
        data = self.get_cleaned_data(validated_data)
        account = UserAccount.objects.create_account(
            password=data.pop('password'), **data)
        return account
