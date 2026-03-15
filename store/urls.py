from django.urls import path
from . import views
# from rest_framework.routers import SimpleRouter
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from pprint import pprint

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

#parent
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
#register child resource
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# pprint(router.urls)
urlpatterns = router.urls + product_router.urls

# urlpatterns = [
#     # defining custom path using router
#     # path('', include(router.urls))

#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetails.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view()),
# ]
