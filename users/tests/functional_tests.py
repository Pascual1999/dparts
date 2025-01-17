from django.test import TestCase, tag

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(TestCase):
    """ Clase base para pruebas """
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('knox_login')
        self.logout_url = reverse('knox_logout')
        self.manage_url = reverse('profile')
        self.change_password_url = reverse('change-password')
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testemail@gmail.com',
            password='testpassword',
            is_business=False,
            name='testname',
            document='12345678',
            contact_number='04141234567',
            address='testaddress',
        )


@tag("functional_tests")
class UsersTests(BaseTestCase):
    """ Pruebas de modulo usuario """

    def test_create_user(self):
        """Prueba de registro de usuario"""
        response = self.client.post(
            self.signup_url,
            {
                    'is_business': False,
                    'name': 'testname',
                    'email': 'testemail1@gmail.com',
                    'document': '1234567',
                    'contact_number': '0414123457',
                    'address': 'testaddress',
                    'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        self.client.post(
            self.signup_url,
            {
                    'is_business': True,
                    'name': 'testbusinessname',
                    'email': 'testemail2@gmail.com',
                    'document': '12345679',
                    'contact_number': '0414123567',
                    'address': 'testaddress',
                    'password': 'testpassword',
            }
        )

        self.assertEqual(User.objects.count(), 3)

    def test_modify_user(self):
        """ Prueba de modificación de usuario"""
        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            self.manage_url,
            {
                'name': 'pascual',
            },
            headers={
                'Authorization': f'Token {response.data["token"]}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(User.objects.get(email='testemail@gmail.com').name,
                         'pascual')

    def test_delete_user(self):
        """ Prueba de borrado de usuario """
        User.objects.create_user(
            email='testemail2@gmail.com',
            password='testpassword',
            is_business=False,
            name='testname',
            document='123456',
            contact_number='04141234567',
            address='testaddress',
        ).save()

        User.objects.get(email='testemail2@gmail.com').delete()

        self.assertEqual(User.objects.count(), 1)

    def test_get_user(self):
        """ Prueba de obtención de usuario """
        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            self.manage_url,
            headers={
                'Authorization': f'Token {response.data["token"]}'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'testname')

    def test_list_users(self):
        """ Prueba de listado de usuarios """
        self.client.post(
            self.signup_url,
            {
                    'is_business': False,
                    'name': 'testname',
                    'email': 'testemail1@gmail.com',
                    'document': '1234567',
                    'contact_number': '0414123457',
                    'address': 'testaddress',
                    'password': 'testpassword',
            }
        )

        self.client.post(
            self.signup_url,
            {
                    'is_business': True,
                    'name': 'testbusinessname',
                    'email': 'testemail2@gmail.com',
                    'document': '12345679',
                    'contact_number': '0414123567',
                    'address': 'testaddress',
                    'password': 'testpassword',
            }
        )

        self.assertEqual(User.objects.count(), 3)

        users = User.objects.all()
        self.assertEqual(users.count(), 3)
        self.assertEqual(users[0].name, 'testname')
        self.assertEqual(users[1].name, 'testname')
        self.assertEqual(users[2].name, 'testbusinessname')


@tag("functional_tests")
class UserAuthTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )
        self.token = response.data['token']

    def test_login(self):
        """Prueba inicio de sesión"""

        response = self.client.get(
            self.manage_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            self.manage_url,
            headers={
                'Authorization': f'Token {response.data["token"]}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """ Prueba de cierre de sesión """
        response = self.client.post(
            self.logout_url,
            headers={
                'Authorization': f'Token {self.token}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(
            self.manage_url
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_change(self):
        """ Prueba de cambio de contraseña """
        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            self.change_password_url,
            {
                'password1': 'testpassword',
                'password2': 'testpassword2',
                'password3': 'testpassword2',
            },
            headers={
                'Authorization': f'Token {response.data["token"]}'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword2',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)