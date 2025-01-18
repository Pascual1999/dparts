from django.test import TestCase, tag


from rest_framework.test import APIClient
\

from ..models import Category, Product, Tag
from ..serializers import CategorySerializer, ProductSerializer


@tag("unit_tests")
class CategoryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cat_data = {"name": "test", "slug": "slugtest"}   
        self.test_cat = Category.objects.create(**self.cat_data)
        self.test_tag = Tag.objects.create(name="testtag", slug="slugtesttag")
        self.test_product = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00,
            tags=[self.test_tag]
        )
        self.test_product2 = Product.objects.create(
            category=self.test_cat,
            name="producttest2",
            sku="test12342",
            slug="producttest2",
            description="product description",
            price=26.00
        )
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

        self.assertEqual(data['products'][0]['name'], self.test_product.name)
        self.assertEqual(data['products'][0]['sku'], self.test_product.sku)
        self.assertEqual(data['products'][0]['get_absolute_url'],
                         self.test_product.get_absolute_url())
        self.assertEqual(data['products'][0]['description'],
                         self.test_product.description)
        self.assertEqual(float(data['products'][0]['price']),
                         self.test_product.price)

        self.assertEqual(data['products'][1]['name'], self.test_product2.name)
        self.assertEqual(data['products'][1]['sku'], self.test_product2.sku)
        self.assertEqual(data['products'][1]['get_absolute_url'],
                         self.test_product2.get_absolute_url())
        self.assertEqual(data['products'][1]['description'],
                         self.test_product2.description)
        self.assertEqual(float(data['products'][1]['price']),
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
                         f"/{self.test_cat.slug}/{self.test_tag.slug}/")
    
    def test_latest_products(self):
        """Prueba de obtención de productos recientes"""
        pass

    def test_search_products(self):
        """Prueba de busqueda de productos"""
        pass

    def test_tag_list(self):
        """Prueba de listado de tags"""
        pass