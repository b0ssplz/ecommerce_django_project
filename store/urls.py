from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


#router = SimpleRouter()
router = DefaultRouter()

router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls)),
    
# ]


# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]
