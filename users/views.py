from django.contrib.auth import login

from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

from knox.views import LoginView as KnoxLoginView

from .serializers import UserSerializer, AuthSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Vista generica para el registro de un nuevo usuario

    Metodo: POST
    Parametros:
        Ver UserSerializer
    """
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    """
    Vista para iniciar sesion y obtener el token de autenticacion.
    Basandose en el login de la libreria knox.

    Metodo: POST
    Parametros:
        email: correo electronico
        password: contraseña
    
    """
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)    


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Vista generica para obtener y actualizar los datos del usuario

    Metodos: GET, PUT y PATCH
    Parametros:
        Ver UserSerializer
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    Vista para cambiar la contraseña del usuario.

    Metodo: POST
    Parametros:
        password1: contraseña actual
        password2: nueva contraseña
        password3: confirmar nueva contraseña
    """
    serializer_class = AuthSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        user = request.user
        auth_data = {'email': user.email, 'password': data['password1']}
        serializer = AuthSerializer(data=auth_data)
        serializer.is_valid(raise_exception=True)
        if data['password2'] == data['password3']:
            user.set_password(data['password2'])
            user.save()
            return Response({'success': 'Contraseña cambiada'})
        else:
            return Response({'error': 'Las contraseñas no coinciden'})
