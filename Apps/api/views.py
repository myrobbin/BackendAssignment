from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, permissions, status, views
from drf_yasg.utils import swagger_auto_schema

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(tags=["Authentication"], operation_summary="Create Account",)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },status=status.HTTP_201_CREATED)



class LoginApi(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=["Authentication"], operation_summary="user Login")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email__iexact=request.data.get('email')).first()
            if not user:
                message = "User name or password is incorrect"
                return Response(
                    {"message": message},
                    status=status.HTTP_404_NOT_FOUND
                )
            if (request.data.get('email')) and request.data.get('password'):
                user = authenticate(username=user.email, password=request.data.get('password'))
            if user:
                token = RefreshToken.for_user(user)

                resp = {
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    'refresh': str(token),
                    'access': str(token.access_token),
                }
                return Response(resp, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User credentials are invalid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserPostView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostUserSerializer

    @swagger_auto_schema(tags=["User Post"], operation_summary="List the authenticated user all post")

    def get(self, request):
        post_obj = Post.objects.filter(author=request.user)
        serializer = self.serializer_class(post_obj,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["User Post"], request_body=serializer_class, operation_summary="Add new post")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            post.author = request.user
            post.save()
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

