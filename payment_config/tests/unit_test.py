from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient

from ..serializers import DollarExchangeHistorySerializer, PaymentMethodSerializer
from ..models import PaymentMethod, PaymentConfig, DollarExchangeHistory
from ..api_calls import get_bcv


User = get_user_model()


@tag('unit_tests')
class PaymentConfigTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testemail@gmailcom',
            password='testpassword',
            is_business=False,
            name='testname',
            document='12345678',
            contact_number='04141234567',
            address='testaddress',
        )
        self.client.force_authenticate(user=self.user)
        self.payment_method = PaymentMethod.objects.create(
            name='test',
            payment_data='testdescription',
            is_active=True
        )
        self.iva = PaymentConfig.objects.create(key='IVA', value=16)

    def test_get_exchange_rate(self):
        """ Prueba de obtención de tasa de cambio """
        ex_data = get_bcv()
        self.assertEqual(ex_data["status_code"], 200)

    def test_get_all_payment_data(self):
        """ Prueba de obtención de datos de pago """
        ex_data = get_bcv()
        self.assertEqual(ex_data["status_code"], 200)

        url = reverse('get_all_payment_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        iva = float(self.iva.value) / 100
        self.assertEqual(response.data['IVA'], iva)
        self.assertEqual(float(response.data['ExchangeRate']),
                         ex_data['obj'].value)

        self.assertEqual(response.data['PaymentMethods'],
                         PaymentMethodSerializer(
                             PaymentMethod.objects.all(), many=True
                             ).data)

    def test_dollar_exchange_serializer(self):
        """ Prueba de serializador de cambio de dolares """
        data = {
            'date': timezone.now(),
            'value': 10,
            'page': 'test.com'
        }

        serializer = DollarExchangeHistorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

        obj = serializer.save()
        self.assertEqual(obj.date, data['date'])
        self.assertEqual(obj.value, data['value'])
        self.assertEqual(obj.page, data['page'])

    def test_payment_method_serializer(self):
        """ Prueba de serializador de metodos de pago """
        data = {
            'name': 'test',
            'payment_data': 'testdescription',
            'key': 'testkey',
            'is_active': True
        }
        obj = PaymentMethod.objects.create(**data)

        serializer = PaymentMethodSerializer(instance=obj)

        self.assertEqual(serializer.data['name'], data['name'])
        self.assertEqual(serializer.data['payment_data'], data['payment_data'])
