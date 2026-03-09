from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from pprint import pprint

router = SimpleRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)
urlpatterns = router.urls

# urlpatterns = [
#     # defining custom path using router
#     # path('', include(router.urls))

#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:pk>/', views.ProductDetails.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view()),
# ]
