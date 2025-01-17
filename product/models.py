from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Modelo de categoría de productos."""
    name = models.CharField('Nombre', max_length=255)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    """Modelo de producto."""
    category = models.ForeignKey(
        Category,
        verbose_name='Categoria',
        related_name='products',
        on_delete=models.CASCADE
        )
    name = models.CharField(
        'Nombre',
        max_length=255
        )
    slug = models.SlugField(
        'URL',
        unique=True
        )
    sku = models.CharField(
        'SKU',
        unique=True,
        blank=False,
        null=True,
        default=None,
        max_length=50
        )
    brand = models.CharField(
        'Marca',
        max_length=64,
        blank=True,
        null=True
    )
    description = models.TextField(
        'Descripción',
        blank=True,
        null=True
        )
    price = models.DecimalField(
        'Precio',
        max_digits=6,
        decimal_places=2
        )
    image = models.ImageField(
        'Imagen',
        upload_to='uploads/',
        blank=True,
        null=True)
    thumbnail = models.ImageField(
        'Miniatura',
        upload_to='uploads/',
        blank=True, null=True)
    date_added = models.DateTimeField(
        'Fecha de agregado',
        auto_now_add=True
        )
    is_active = models.BooleanField(
        'Activo?',
        default=True
        )
    tags = models.ManyToManyField(
        to='Tag',
        blank=True,
        through='ProductTag'
    )

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(600, 400)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.sku)
        super(Product, self).save(*args, **kwargs)


class Tag(models.Model):
    """Modelo de etiqueta."""
    name = models.CharField(
        'Nombre',
        max_length=255
        )
    Category = models.ForeignKey(
        Category,
        verbose_name='Categoría',
        related_name='tags',
        on_delete=models.CASCADE
        )
    slug = models.SlugField(
        'URL',
        unique=True
        )
    products = models.ManyToManyField(
        Product,
        blank=True,
        through='ProductTag'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'etiqueta'
        verbose_name_plural = 'etiquetas'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tag/{self.slug}/'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class ProductTag(models.Model):
    """Modelo auxiliar de etiqueta de producto."""
    product = models.ForeignKey(
        Product,
        verbose_name='Producto',
        related_name='product_tags',
        on_delete=models.CASCADE
        )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Etiqueta',
        related_name='product_tags',
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = 'etiqueta de producto'
        verbose_name_plural = 'etiquetas de productos'
