from django.urls import path

from product import views


urlpatterns = [
    path('latest-products', views.LatestProductsList.as_view(),
         name="latest_products"),
    path('related-products/', views.RelatedProductsList.as_view(),
         name="related_products"),
    path("products/search", views.search, name="search"),
    path('products/tag/<slug:tag_slug>/', views.ListByTag.as_view(),
         name="products_by_tag"),
    path('products/tags/', views.ListByTags.as_view(),
         name="products_by_tags"),
    path('tag-list/', views.TagList.as_view(), name="tag_list"),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductDetail.as_view(), name="product_detail"),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view(), 
         name="category_detail"),
]
