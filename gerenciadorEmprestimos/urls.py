from django.urls import include, path
from rest_framework import routers
from views import views

router = routers.DefaultRouter()
router.register(r'loans', views.LoanViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('views', include(router.urls)),
]
