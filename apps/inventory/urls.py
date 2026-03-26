# apps/inventory/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stocks', views.StockViewSet, basename='stock')

urlpatterns = router.urls

__all__ = ['urlpatterns']
