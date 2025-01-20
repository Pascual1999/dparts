from django.test import TestCase, tag
from django.urls import reverse

from time import sleep

from rest_framework.test import APIClient


from ..models import Category, Product, Tag
from ..serializers import CategorySerializer, ProductSerializer


@tag("unit_tests")
class ProductCategoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.latest_products_url = reverse('latest_products')
        self.search_url = reverse("search")
        self.tag_list_url = reverse("tag_list")
        self.cat_data = {"name": "test", "slug": "slugtest"}   
        self.test_cat = Category.objects.create(**self.cat_data)
        self.test_tag = Tag.objects.create(
            name="testtag",
            Category=self.test_cat,
            slug="slugtesttag")
        self.test_product = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        sleep(1)
        self.test_product2 = Product.objects.create(
            category=self.test_cat,
            name="producttest2",
            sku="test12342",
            slug="producttest2",
            description="product description",
            price=26.00
        )
        sleep(1)
        self.serializer = CategorySerializer(instance=self.test_cat)
        self.p_serializer = ProductSerializer(instance=self.test_product)

    def test_category_get_absolute_url(self):
        """Prueba de obtención de url de categoría"""
        self.assertEqual(self.test_cat.get_absolute_url(),
                         f"/{self.cat_data['slug']}")

    def test_category_serializer(self):
        """Prueba de serialización de categoría"""
        data = self.serializer.data

        self.assertEqual(data['name'], self.cat_data['name'])

        self.assertEqual(data['get_absolute_url'],
                         self.test_cat.get_absolute_url())

        self.assertEqual(data['products'][1]['name'], self.test_product.name)
        self.assertEqual(data['products'][1]['sku'], self.test_product.sku)
        self.assertEqual(data['products'][1]['get_absolute_url'],
                         self.test_product.get_absolute_url())
        self.assertEqual(data['products'][1]['description'],
                         self.test_product.description)
        self.assertEqual(float(data['products'][1]['price']),
                         self.test_product.price)

        self.assertEqual(data['products'][0]['name'], self.test_product2.name)
        self.assertEqual(data['products'][0]['sku'], self.test_product2.sku)
        self.assertEqual(data['products'][0]['get_absolute_url'],
                         self.test_product2.get_absolute_url())
        self.assertEqual(data['products'][0]['description'],
                         self.test_product2.description)
        self.assertEqual(float(data['products'][0]['price']),
                         self.test_product2.price)

        self.assertNotIn('slug', data)
    
    def test_product_get_absolute_url(self):
        """Prueba de obtención de url de producto"""
        self.assertEqual(self.test_product.get_absolute_url(),
                         f"/{self.test_cat.slug}/{self.test_product.slug}/")

    def test_product_serializer(self):
        """Prueba de serialización de productos"""

        data = self.p_serializer.data

        self.assertEqual(data['name'], self.test_product.name)

        self.assertEqual(data['get_absolute_url'],
                         self.test_product.get_absolute_url())

        self.assertEqual(data['category'], self.test_cat.id)

        self.assertEqual(data['id'], self.test_product.id)
        self.assertEqual(data['sku'], self.test_product.sku)
        self.assertEqual(data['description'], self.test_product.description)
        self.assertEqual(float(data['price']), self.test_product.price)

        self.assertNotIn('slug', data)

    def test_tag_get_absolute_url(self):
        """Prueba de obtención de url de tag"""
        self.assertEqual(self.test_tag.get_absolute_url(),
                         f"/tag/{self.test_tag.slug}/")

    def test_latest_products(self):
        """Prueba de obtención de productos recientes"""
        self.test_product3 = Product.objects.create(
            category=self.test_cat,
            name="producttest3",
            sku="test12343",
            slug="producttest3",
            description="product description",
            price=26.00
        )
        sleep(1)
        self.test_product4 = Product.objects.create(
            category=self.test_cat,
            name="producttest4",
            sku="test12344",
            slug="producttest4",
            description="product description",
            price=26.00
        )
        sleep(1)
        self.test_product5 = Product.objects.create(
            category=self.test_cat,
            name="producttest5",
            sku="test12345",
            slug="producttest5",
            description="product description",
            price=26.00
        )

        response = self.client.get(self.latest_products_url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 4)

        self.assertEqual(response.data[0]['name'], self.test_product5.name)
        self.assertEqual(response.data[0]['sku'], self.test_product5.sku)
        self.assertEqual(response.data[0]['get_absolute_url'],
                         self.test_product5.get_absolute_url())
        self.assertEqual(response.data[0]['description'],
                         self.test_product5.description)
        self.assertEqual(float(response.data[0]['price']),
                         self.test_product5.price)

        self.assertEqual(response.data[3]['name'], self.test_product2.name)
        self.assertEqual(response.data[3]['sku'], self.test_product2.sku)
        self.assertEqual(response.data[3]['get_absolute_url'],
                         self.test_product2.get_absolute_url())
        self.assertEqual(response.data[3]['description'],
                         self.test_product2.description)
        self.assertEqual(float(response.data[3]['price']),
                         self.test_product2.price)


    def test_search_products(self):
        """Prueba de busqueda de productos"""
        self.test_product3 = Product.objects.create(
            category=self.test_cat,
            name="busqueda",
            sku="test12343",
            slug="producttest3",
            description="product description",
            price=26.00
        )

        response = self.client.post(
            self.search_url,
            {'query': 'busqueda'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['name'], self.test_product3.name)
        self.assertEqual(response.data[0]['sku'], self.test_product3.sku)
        self.assertEqual(response.data[0]['get_absolute_url'],
                         self.test_product3.get_absolute_url())
        self.assertEqual(response.data[0]['description'],
                         self.test_product3.description)
        self.assertEqual(float(response.data[0]['price']),
                         self.test_product3.price)

    def test_tag_list(self):
        """Prueba de listado de tags"""

        response = self.client.get(self.tag_list_url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['name'], self.test_tag.name)

        response = self.client.get(
            self.tag_list_url,
            {'category': self.test_cat.name})
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['name'], self.test_tag.name)