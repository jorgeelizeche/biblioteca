from django.urls import path
from .views import RegistroView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegistroView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

]
