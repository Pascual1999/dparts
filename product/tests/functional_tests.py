from django.test import TestCase, tag


from rest_framework.test import APIClient
from rest_framework import status


from ..models import Category, Product

@tag("functional_tests")
class CategoryTests(TestCase):
    """Pruebas del modulo categorias"""
    def setUp(self):
        self.base_url = "/api/v1/products/"
        self.client = APIClient()

    def test_category_creation(self):
        """Prueba de registro de categorias"""

        Category.objects.create(
            name="nametest",
            slug="nametest",
        )

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.all()[0].name, "nametest")

        Category.objects.create(
            name="nametest2",
            slug="nametest2",
        )

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.all()[1].name, "nametest2")

    def test_category_get(self):
        """Prueba de obtención de categoria"""

        Category.objects.create(
            name="nametest",
            slug="slugtest",
        )
        test_cat = Category.objects.get(slug="slugtest")

        self.assertEqual(Category.objects.count(), 1)
        response = self.client.get(
            self.base_url + f"{test_cat.slug}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["name"], "nametest")

    def test_category_modify(self):
        """Prueba de modificacion de categoria"""
        Category.objects.create(
            name="nametest",
            slug="slugtest",
        )
        self.assertEqual(Category.objects.get(id=1).name, "nametest")
        self.assertEqual(Category.objects.get(id=1).slug, "slugtest")
        test_cat = Category.objects.get(slug="slugtest")

        test_cat.name = "nametest2"
        test_cat.slug = "slugtest2"

        test_cat.save()

        self.assertEqual(Category.objects.all().count(), 1)
        self.assertEqual(Category.objects.get(id=1).name, "nametest2")
        self.assertEqual(Category.objects.get(id=1).slug, "slugtest2")

    def test_category_list(self):
        """Prueba para listar categorias"""
        Category.objects.create(
            name="nametest",
            slug="slugtest",
        )
        Category.objects.create(
            name="nametest2",
            slug="slugtest2",
        )
        Category.objects.create(
            name="nametest3",
            slug="slugtest3",
        )

        test_cat_list = Category.objects.all()

        self.assertEqual(test_cat_list.count(), 3)
        self.assertEqual(test_cat_list[0].name, "nametest")
        self.assertEqual(test_cat_list[1].name, "nametest2")
        self.assertEqual(test_cat_list[2].name, "nametest3")

    def test_category_delete(self):
        """Prueba de eliminación de categorias"""
        Category.objects.create(
            name="nametest",
            slug="slugtest",
        )
        Category.objects.create(
            name="nametest2",
            slug="slugtest2",
        )
        Category.objects.create(
            name="nametest3",
            slug="slugtest3",
        )

        test_cat_list = Category.objects.all()

        self.assertEqual(test_cat_list.count(), 3)

        Category.objects.get(slug="slugtest2").delete()

        self.assertEqual(Category.objects.all().count(), 2)

        self.assertEqual(Category.objects.all()[0].name, "nametest")
        self.assertEqual(Category.objects.all()[1].name, "nametest3")


@tag("functional_tests")
class ProductTest(TestCase):

    def setUp(self):
        self.base_url = "/api/v1/products/"
        self.client = APIClient()
        self.test_cat = Category.objects.create(
            name="test",
            slug="slugtest"
        )

    def test_product_creation(self):
        """Prueba de registro de productos"""

        test_product = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        
        test_product.save()

        products = Product.objects.all()

        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].name, "producttest")
        self.assertEqual(products[0].price, 25.00)
    
    def test_product_get(self):
        """Prueba de obtención de productos"""

        test_product = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        
        products = Product.objects.all()

        self.assertEqual(products.count(), 1)

        response = self.client.get(
            self.base_url + f"{self.test_cat.slug}/{test_product.slug}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "producttest")
        
    def test_product_list(self):
        """Prueba de lista de productos"""

        Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        Product.objects.create(
            category=self.test_cat,
            name="producttest2",
            sku="test12342",
            slug="producttest2",
            description="product description",
            price=26.00
        )
        Product.objects.create(
            category=self.test_cat,
            name="producttest3",
            sku="test12343",
            slug="producttest3",
            description="product description",
            price=27.00
        )

        products = Product.objects.all().order_by("id")

        self.assertEqual(products.count(), 3)
        self.assertEqual(products[0].name, 'producttest')
        self.assertEqual(products[1].name, 'producttest2')
        self.assertEqual(products[2].name, 'producttest3')

    def test_product_modify(self):
        """Prueba de modificación de productos"""
        test_product = Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )

        test_product.name = "producttest32"
        test_product.price = 28.32
        test_product.save()

        self.assertEqual(Product.objects.get(slug="producttest").name,
                         "producttest32")
        self.assertAlmostEqual(float(Product.objects.get(id=1).price),
                               28.32, places=2)

    def test_product_delete(self):
        """Prueba de eliminación de productos"""
        Product.objects.create(
            category=self.test_cat,
            name="producttest",
            sku="test1234",
            slug="producttest",
            description="product description",
            price=25.00
        )
        Product.objects.create(
            category=self.test_cat,
            name="producttest2",
            sku="test12342",
            slug="producttest2",
            description="product description",
            price=26.00
        )
        Product.objects.create(
            category=self.test_cat,
            name="producttest3",
            sku="test12343",
            slug="producttest3",
            description="product description",
            price=27.00
        )

        self.assertEqual(Product.objects.all().count(), 3)

        Product.objects.get(slug="producttest2").delete()

        self.assertEqual(Product.objects.all().count(), 2)
        self.assertEqual(Product.objects.all().order_by("id")[0].name,
                         "producttest")
        self.assertEqual(Product.objects.all().order_by("id")[1].name,
                         "producttest3")
        
