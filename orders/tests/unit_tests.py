from django.test import TestCase, tag
from django.contrib.auth import get_user_model


from rest_framework.test import APIClient

from product.models import Category, Product
from orders.models import Order, OrderItem
from orders.serializers import MyOrderSerializer, OrderSerializer

User = get_user_model()


@tag("unit_tests")
class OrderUnitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testemail@gmail.com",
            password="test_password"
        )
        self.producttest = Product.objects.create(
            name="test_product",
            description="test_description",
            price=10.00,
            category=Category.objects.create(name="test_category"),
        )

        self.order_data = {
            "items": [{"product": self.producttest.id, "quantity": 2,
                       "price": self.producttest.price}],
            "shipping_address": "test_address",
            "contact_number": "test_number",
            "amount": "20.00",
            "status": Order.IN_PROGRESS
        }
        self.create_order_serializer = OrderSerializer(data=self.order_data)
        self.view_order_serializer = MyOrderSerializer

    def test_create_order_serializer(self):
        """ Prueba del serializador de ordenes """
        self.assertTrue(self.create_order_serializer.is_valid(raise_exception=True))

        order = self.create_order_serializer.save(user=self.user)

        self.assertEqual(order.status, Order.IN_PROGRESS)

        self.assertEqual(order.user, self.user)

        self.assertEqual(order.items.count(), 1)

        self.assertEqual(order.items.first().product, self.producttest)
        self.assertEqual(order.items.first().quantity, 2)
        self.assertEqual(order.items.first().price, self.producttest.price)

        self.assertEqual(order.amount, 20.00)
        self.assertEqual(order.shipping_address, "test_address")
        self.assertEqual(order.contact_number, "test_number")
        self.assertEqual(order.status, Order.IN_PROGRESS)

    def test_view_order_serializer(self):
        """ Prueba del serializador para la visualización de ordenes """
        order = Order.objects.create(
            user=User.objects.get(email="testemail@gmail.com"),
            shipping_address=self.order_data["shipping_address"],
            contact_number=self.order_data["contact_number"],
            amount=self.order_data["amount"],
            status=self.order_data["status"]
        )
        OrderItem.objects.create(
            order=order,
            product=self.producttest,
            quantity=2,
            price=self.producttest.price
            )
        
        serialized_order = self.view_order_serializer(instance=order).data

        self.assertEqual(serialized_order["id"], order.id)
        self.assertEqual(serialized_order["shipping_address"],
                         order.shipping_address)
        self.assertEqual(serialized_order["contact_number"],
                         order.contact_number)
        self.assertEqual(serialized_order["status"], order.status)
        self.assertEqual(serialized_order["amount"], order.amount)

        self.assertEqual(serialized_order["items"][0]["product"]["id"],
                         order.items.first().product.id)

        self.assertEqual(serialized_order["items"][0]["quantity"],
                         order.items.first().quantity)
        self.assertEqual(float(serialized_order["items"][0]["price"]),
                         order.items.first().price)
        
    def test_order_paid_but_no_proof(self):
        """ Prueba de invalidación de ordenes pagadas sin comprobante """
        order = Order.objects.create(
            user=User.objects.get(email="testemail@gmail.com"),
            shipping_address=self.order_data["shipping_address"],
            contact_number=self.order_data["contact_number"],
            amount=self.order_data["amount"],
            status=self.order_data["status"]
        )
        OrderItem.objects.create(
            order=order,
            product=self.producttest,
            quantity=2,
            price=self.producttest.price
            )
        self.assertEqual(order.status, Order.IN_PROGRESS)

        order.status = Order.PAID

        self.assertRaises(Exception, order.save)
    
    def test_order_item_product_name(self):
        """ Prueba de respaldo del nombre del producto de los articulos de la orden """
        order = Order.objects.create(
            user=User.objects.get(email="testemail@gmail.com"),
            shipping_address=self.order_data["shipping_address"],
            contact_number=self.order_data["contact_number"],
            amount=self.order_data["amount"],
            status=self.order_data["status"]
        )
        OrderItem.objects.create(
            order=order,
            product=self.producttest,
            quantity=2,
            price=self.producttest.price
            )
        self.assertEqual(order.items.first().product_name,
                         self.producttest.name)

