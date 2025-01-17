import tempfile
import PIL
import json

from django.test import TestCase, tag
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone


from rest_framework.test import APIClient
from rest_framework import status

from product.models import Category, Product
from orders.models import Order
from payment_config.models import (
    PaymentMethod, PaymentConfig, DollarExchangeHistory
    )

User = get_user_model()


@tag("functional_tests")
class OrderTests(TestCase):

    def setUp(self):
        self.login_url = reverse("knox_login")
        self.new_order_url = reverse("new_order")
        self.order_list_url = reverse("order_list")
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
        response = self.client.post(
            self.login_url,
            {
                'username': 'testemail@gmail.com',
                'password': 'testpassword',
            }
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + response.data["token"])
        self.token = response.data["token"]
        self.test_cat = Category.objects.create(
            name="test",
            slug="slugtest"
        )
        self.producttest = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        self.producttest2 = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1235",
            slug="producttest2",
            description="product description",
            price=23.00
        )
        self.iva = float(PaymentConfig.objects.create(
            key="IVA",
            value=16
        ).value) / 100
        self.payment_method = PaymentMethod.objects.create(
            name="Efectivo",
            payment_data="test payment data",
            is_active=True
        )
        self.exchange_rate = DollarExchangeHistory.objects.create(
            date=timezone.now(),
            value=51.50,
            page="https://dolarhoy.com/"
        )

    def test_order_creation(self):
        """Prueba de registro de orden"""

        items = [
            {
                "product": self.producttest.id,
                "quantity": 1,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        response = self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        orders = Order.objects.all()

        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders[0].items.count(), 2)
        self.assertEqual(orders[0].items.all()[0].product, self.producttest)
        self.assertEqual(orders[0].items.all()[1].product, self.producttest2)
        self.assertEqual(orders[0].items.all()[0].quantity, 1)
        self.assertEqual(orders[0].items.all()[1].quantity, 3)
        self.assertEqual(orders[0].items.all()[0].price,
                         self.producttest.price)
        self.assertEqual(orders[0].items.all()[1].price,
                         self.producttest2.price)
        self.assertEqual(orders[0].shipping_address, "test address")
        self.assertEqual(orders[0].contact_number, "04141234567")
        self.assertEqual(orders[0].status, Order.IN_PROGRESS)

        amount = ((self.producttest.price * 1) + 
                  (self.producttest2.price * 3))
        amount = (amount * (1 + (float(self.iva))))

        self.assertAlmostEqual(float(orders[0].amount),
                               float(amount), places=2)

    def test_order_list(self):
        """Prueba de listado de ordenes"""
        response = self.client.get(self.order_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = [
            {
                "product": self.producttest.id,
                "quantity": 1,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )
        items = [
            {
                "product": self.producttest.id,
                "quantity": 4,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )

        response = self.client.get(self.order_list_url)

        orders = Order.objects.all()
        orders_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(orders.count(), 2)
        self.assertEqual(orders_json[0]["id"], orders[0].id)
        self.assertEqual(orders_json[0]["shipping_address"],
                         orders[0].shipping_address)
        self.assertEqual(orders_json[0]["contact_number"],
                         orders[0].contact_number)
        self.assertEqual(orders_json[1]["id"], orders[1].id)
        self.assertEqual(orders_json[1]["shipping_address"],
                         orders[1].shipping_address)
        self.assertEqual(orders_json[1]["contact_number"],
                         orders[1].contact_number)

    def test_order_detail(self):
        """Prueba de obtención de ordenes"""
        items = [
            {
                "product": self.producttest.id,
                "quantity": 1,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        response = self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )

        order = Order.objects.all()[0]

        response = self.client.get(reverse("get_order", args=[order.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], order.id)
        self.assertEqual(response.data["shipping_address"], "test address")
        self.assertEqual(response.data["contact_number"], "04141234567")

    def test_order_modify(self):
        """Prueba de modificación de ordenes"""
        items = [
            {
                "product": self.producttest.id,
                "quantity": 1,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        response = self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )

        order = Order.objects.all()[0]
        self.assertEqual(order.status, Order.IN_PROGRESS)

        image = PIL.Image.new('RGB', size=(400, 300), color=(255, 0, 0))
        file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(file)
        file.seek(0)
        with open(file.name, 'rb') as f:
            file = f
            uploaded_file = SimpleUploadedFile(file.name, file.read(),
                                               content_type='multipart/form-data')
            
            response = self.client.patch(
                reverse("update_order", args=[order.id]),
                {"payment_method": self.payment_method.id,
                    "proof_of_payment": uploaded_file},
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        orders = Order.objects.all()
        self.assertEqual(orders[0].payment_method, self.payment_method)
        self.assertEqual(orders[0].status, Order.PAID)
        with open(file.name, 'rb') as f:
            from os.path import basename
            self.assertEqual(basename(orders[0].proof_of_payment.name),
                             basename(f.name))
            
    def test_order_delete(self):
        """Prueba de eliminación de ordenes"""
        items = [
            {
                "product": self.producttest.id,
                "quantity": 1,
                "price": self.producttest.price
            },
            {
                "product": self.producttest2.id,
                "quantity": 3,
                "price": self.producttest2.price
            }
        ]

        self.client.post(
            self.new_order_url,
            {
                "shipping_address": "test address",
                "contact_number": "04141234567",
                "items": items
            },
            format="json"
        )

        order = Order.objects.all()[0]

        self.assertEqual(Order.objects.all().count(), 1)

        Order.objects.get(id=order.id).delete()

        self.assertEqual(Order.objects.all().count(), 0)
