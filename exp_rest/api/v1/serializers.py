from rest_framework import serializers

from exp_rest.login import login


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=80)

    def login(self):
        data = self.validated_data
        email = data['email']
        password = data['password']
        token = login(email, password)
        return token

    class Meta:
        fields = ('email', 'password')