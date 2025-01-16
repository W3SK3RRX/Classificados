from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.api.viewsets import UserViewSet, PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('plans', PlanViewSet, basename='plan')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('perfil-profissional/', include('perfil_profissional.urls')),
    path('users/', include('users.urls')),  # Incluindo as rotas do app 'users'
]
