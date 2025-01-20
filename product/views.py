# from django.shortcuts import render

from django.http import Http404
from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category, Tag
from .serializers import (ProductSerializer, CategorySerializer,
                          TagSerializer, SimpleTagSerializer)


class LatestProductsList(generics.ListAPIView):
    """
    Vista para obtener los 4 productos mas recientes

    Método: GET
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        products = Product.objects.filter(
            is_active=True
            )[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class RelatedProductsList(generics.ListAPIView):
    """
    Vista para 4 productos relacionados con a otro
    a través de sus etiquetas.

    Método: GET
    Parámetros:
        product_id: id del producto base
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.filter(is_active=True)   

    def get(self, request, format=None):
        product_id = request.query_params.get('product_id', None)
        try:
            tags = Product.objects.get(id=product_id).tags.all()
            products = Product.objects.filter(
                is_active=True,
                tags__in=tags).exclude(id=product_id)[0:4]
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404


class ProductDetail(APIView):
    """
    Vista para obtener los detalles de un producto.

    Método: GET
    Parámetros:
        category_slug: slug de la categoria
        product_slug: slug del producto
    """
    permission_classes = (permissions.AllowAny,)

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug,
                                          is_active=True).get(
                                          slug=product_slug)
        except Product.DoesNotExist or Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryDetail(APIView):
    """
    Vista para obtener los productos de una categoría.

    Método: GET
    Parámetros:
        category_slug: slug de la categoria
    """
    permission_classes = (permissions.AllowAny,)

    def get_object(self, category_slug):
        try:
            return Category.objects.get(
                slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):

        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class ListByTags(generics.ListAPIView):
    """
    Vista para obtener una lista de productos en base a una o
    más etiquetas.

    Método: GET
    Parámetros:
        tags: id de las etiquetas
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        filter = self.request.query_params.get('tags', None)
        if filter is not None and filter != '':
            tags = filter.split(',')
            products = Product.objects.all()
            for tag in tags:
                products = products.filter(tags__id=tag, is_active=True)
            return products
        else:
            return None


class ListByTag(APIView):
    """
    Vista para obtener una lista de productos en base a una etiqueta.

    Método: GET
    Parámetros:
        tag_slug: slug de la etiqueta
    """
    permission_classes = (permissions.AllowAny,)

    def get_object(self, tag_slug):
        try:
            return Tag.objects.get(
                slug=tag_slug)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, tag_slug, format=None):
        tag = self.get_object(tag_slug)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class TagList(generics.ListAPIView):
    """
    Vista para obtener una lista de las etiquetas relacionadas 
    a una categoría.

    Método: GET
    Parámetros:
        category: nombre de la categoria
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        category_name = request.query_params.get('category', None)
        if category_name is not None:
            try:
                tags = Tag.objects.filter(Category__name=category_name)
            except Category.DoesNotExist:
                raise Http404
        else:
            tags = Tag.objects.all()
        serializer = SimpleTagSerializer(tags, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    """
    Vista para obtener una lista de productos relacionados
    a un termino de busqueda con parametros para filtrar por
    categoria y etiqueta.

    Método: POST
    Parámetros:
        query: termino de busqueda
        category: nombre de la categoria
        tags: ids de las etiquetas
    """

    query = request.data.get('query', '')
    category = request.data.get('category', '')
    tags = request.data.get('tags', '')
    if query:
        products = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query))
        if category:
            products = products.filter(category__name=category)
            if tags:
                tags = tags.split(',')
                for tag in tags:
                    products = products.filter(tags__id=tag)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []})
