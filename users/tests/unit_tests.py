from django.test import TestCase, tag

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


from django.contrib.auth import get_user_model

from users.serializers import UserSerializer, AuthSerializer

User = get_user_model()


@tag("unit_tests")
class UserUnitTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.signup_url = reverse('signup')
        self.login_url = reverse('knox_login')
        self.logout_url = reverse('knox_logout')
        self.manage_url = reverse('profile')

        self.user_data = {
            "email": 'testemail@gmail.com',
            "password": 'testpassword',
            "is_business": False,
            "name": 'testname',
            "document": '12345678',
            "contact_number": '04141234567',
            "address": 'testaddress'
        }
        self.user_login_data = {
            "email": 'testemail@gmail.com',
            "password": 'testpassword'
        }

        self.user_serializer = UserSerializer(data=self.user_data)
        self.auth_serializer = AuthSerializer(data=self.user_login_data)

    def test_user_validation(self):
        """ Prueba de validación datos de usuario """
        response = self.client.post(self.signup_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.signup_url, {
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'is_business': False,
            'name': 'testname',
            'document': '12345678',
            'contact_number': '04141234567',
            'address': 'testaddress',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.signup_url, {
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'is_business': False,
            'name': 'testname',
            'document': '12345678',
            'contact_number': '04141234567',
            'address': 'testaddress',
        })

        # Verificar que el correo sea unico

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.signup_url, {
            'email': 'testemail1@gmail.com',
            'password': 'testpassword',
            'is_business': False,
            'name': 'testname',
            'document': '12345678',
            'contact_number': '04141234567',
            'address': 'testaddress',
        })
        # Verificar que el documento sea unico
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_serializer(self):
        """ Prueba de serializador de usuario """
        try:
            self.user_serializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail(e)

        data = self.user_serializer.data

        self.assertEqual(data['email'], self.user_data['email'])
        self.assertEqual(data['name'], self.user_data['name'])
        self.assertEqual(data['document'], self.user_data['document'])
        self.assertEqual(data['contact_number'],
                         self.user_data['contact_number'])
        self.assertEqual(data['address'], self.user_data['address'])
        self.assertEqual(data['is_business'], self.user_data['is_business'])

        self.assertNotIn('password', data)

    def test_auth_serializer(self):
        """ Prueba de serializador de autenticación de usuario """
        self.client.post(self.signup_url, {
            'email': 'testemail@gmail.com',
            'password': 'testpassword',
            'is_business': False,
            'name': 'testname',
            'document': '12345678',
            'contact_number': '04141234567',
            'address': 'testaddress',
        })

        # Datos validos
        try:
            self.auth_serializer.is_valid(raise_exception=True)
        except Exception as e:
            self.fail(e)

        # Datos invalidos

        wrong_email_user_data = {
            "email": 'testemail1@gmail.com',
            "password": 'testpassword'
        }

        auth_serializer = AuthSerializer(data=wrong_email_user_data)

        self.assertRaises(Exception, auth_serializer.is_valid,
                          raise_exception=True)

        wrong_password_user_data = {
            "email": 'testemail@gmail.com',
            "password": 'testpassword1'
        }

        auth_serializer = AuthSerializer(data=wrong_password_user_data)
        
        self.assertRaises(Exception, auth_serializer.is_valid,
                          raise_exception=True)


