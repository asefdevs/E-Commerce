from rest_framework import serializers
from accounts.models import CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['username', 'password', 'first_name', 'last_name', 'email', 'password2']
        extra_kwargs={'password':{'write_only':True}}


    def create(self,validated_data):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        email=self.validated_data['email']
        username=self.validated_data['username']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords do not match'})
        user=CustomUser.objects.create(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return user
    def validate_username(self,value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({'username':f'username :This username > {value} is already in use'})
        return value
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email':f' This email > {value} already exists'})
        return value
    def validate_password(self, value):
        if len(value)<8:
            raise serializers.ValidationError({'password':'Password must be at least 8 characters'})
        return value

