from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,UserLoginSerializer,UserProfileSerializer,ProfilePhotoUpdateSerializer
from accounts.models import CustomUser,UserProfile
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.exceptions import NotFound

class RegisterApiView(APIView):
    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class LoginApiView(APIView):
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password'] 
            user=authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserProfileSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self):
        user=self.request.user
        try:
            profile=UserProfile.objects.get(user=user)
        except CustomUser.DoesNotExist:
            raise NotFound('User does not exist')
        return profile
    
class ChangeProfilePhoto(generics.UpdateAPIView):
    serializer_class=ProfilePhotoUpdateSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self):
        user=self.request.user
        try:
            profile=UserProfile.objects.get(user=user)
        except CustomUser.DoesNotExist:
            raise NotFound('Profile does not exist')
        return profile


