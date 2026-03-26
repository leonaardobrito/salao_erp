# apps/customers/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.CustomerViewSet, basename='customer')

urlpatterns = router.urls

__all__ = ['urlpatterns']
