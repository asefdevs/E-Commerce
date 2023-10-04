from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from accounts.models import CustomUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
class RegisterApiView(APIView):
    def post(self,request):
        serializer=UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

        



