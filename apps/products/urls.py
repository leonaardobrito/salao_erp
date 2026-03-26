# apps/products/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ProductViewSet, basename='product')

urlpatterns = router.urls

__all__ = ['urlpatterns']
