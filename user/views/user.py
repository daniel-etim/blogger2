from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers.auth import LoginSerializer
from user.serializers.user import RegisterModelSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: Request):
    serializer = RegisterModelSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(
        data={
            "message": "Successfully Registered", 
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        },
        status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    clean_data = serializer.validated_data

    user = authenticate(username=clean_data["email"], password=clean_data["password"])

    if not user:
        return Response(data={"error": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    return Response(
        data={
            "message": "Login Successful", 
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(access),
        }, 
        
        status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request: Request):
    pass

@api_view(['GET'])
def dashboard(request: Request, pk: int):
    pass