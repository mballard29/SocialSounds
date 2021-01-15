from django.contrib.auth import get_user_model
from django.conf import settings as django_settings
from rest_framework import status
from rest_framework.response import Response
from .utils import AuthTools
from api import settings as api_settings
from api import generics
from api.auth import serializers as auth_serializers
from api.serializers import UserSerializer, ProfileSerializer
from api.models import Profile
from rest_framework.views import APIView 
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect, reverse
from django.contrib import messages 

# These authentication serializers are modeled from the tutorial from Education Ecosystem on YouTube (cited in README).

User = get_user_model()

class UserView(generics.RetrieveUpdateAPIView):

    model = User
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get_object(self, *args, **kwargs):
        return self.request.user

class ProfileView(generics.RetrieveUpdateAPIView):
    model = User.profile
    serializer_class = ProfileSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get_object(self, *args, **kwargs):
        return self.request.user.profile

class LoginView(generics.GenericAPIView):
    template_view = '../templates/api/login.html'
    permission_classes = api_settings.UNPROTECTED
    serializer_class = auth_serializers.LoginSerializer

    def get(self, request): 
        return render(request, self.template_view)

    def post(self, request):
        # print(request.data)
        if 'email' in request.data and 'password' in request.data:

            email = request.data['email'].lower()
            password = request.data['password']

            # returns None or user instance
            user = AuthTools.authenticate_email(email, password)

            # logs in if not None
            if user is not None and AuthTools.login(request, user):
                token = AuthTools.issue_user_token(user, 'login')
                serializer = auth_serializers.LoginCompleteSerializer(token)
                return redirect('/api/items/')

            else: 
                messages.error(request, "Invalid username or password.")

        # return render(request, '../templates/api/login.html')
        return render(request, template_name=self.template_view)
        # send message if we did not return above
        # message = {'message': 'Not able to login (could not use credentials).'}
        # return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):

    permission_classes = api_settings.CONSUMER_PERMISSIONS
    serializer_class = auth_serializers.LogoutSerializer

    def get(self, request):
        return redirect('/')

    def post(self, request):
        if AuthTools.logout(request):
            data = {"logout": "success"}

            # return request ok
            return Response(data, status=status.HTTP_200_OK)

        # return bad request if we did not return above
        return Response(status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    template_view = '../templates/api/register.html'
    template_name=[TemplateHTMLRenderer]

    permission_classes = api_settings.UNPROTECTED
    serializer_class = auth_serializers.UserRegisterSerializer

    def post(self, request): 
        if 'first_name' in request.data and 'last_name' in request.data and 'username' in request.data and 'password' in request.data and 'email' in request.data: 
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            username = request.data['username']
            email = request.data['email'].lower()
            password = request.data['password']

            if first_name != "" and last_name != "" and username != "" and email != "" and password != "": 
                blob = AuthTools.register(request.data, username, 'consumer_basic')
                if blob['is_new'] == True:
                    return redirect('/api/auth/login/')
                else: 
                    messages.error(request, "Invalid username or password.")
                    return render(request, template_name=self.template_view)
            else: 
                messages.error(request, "Missing form fields.")
                return render(request, template_name=self.template_view,)

        return render(request, template_name=self.template_view)

    def get(self, request): 
        return render(request, self.template_view)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)





