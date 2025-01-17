from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'name',
            'email',
            'is_business',
            'document',
            'contact_number',
            'address',
            'description',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_password = validated_data.pop('password')

        user = get_user_model().objects.create(**validated_data)

        user.set_password(validated_password)
        user.save()

        return user


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = ('No se pudo autenticar con las credenciales proporcionadas')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
