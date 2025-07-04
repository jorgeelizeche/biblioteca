from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import GeneroViewSet, AutorViewSet, LibroViewSet, CalificacionViewSet

router = DefaultRouter()
router.register(r'generos', GeneroViewSet)
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
