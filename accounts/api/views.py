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
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
import secrets
from django.urls import reverse
class RegisterApiView(APIView):
    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        token = secrets.token_urlsafe(32)
        user_email=user.email
        user.email_verification_token = token
        user.save()
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        verification_link = 'http://'+current_site + \
                relativeLink+"?token="+str(token)
        send_mail(
            'Email Verification',
            f'Click the link to verify your email: {verification_link}',
            'sender@example.com',  
            [user_email],
            fail_silently=False,
        )        
        return Response({'message': f'Please check your email for verification'})


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            user.is_verified = True
            user.email_verification_token = None
            user.save()
            return Response({'message': 'Successfully verified'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token or user not found'}, status=status.HTTP_404_NOT_FOUND)
        

class LoginApiView(APIView):
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password'] 
            try:
                user=CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise Exception('User doesnt exist')
            if user.is_verified == True:
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
            else:
                return Response({'detail': 'This account is not verified'})
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


