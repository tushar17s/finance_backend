from django.urls import path
from .views import record_list_create, record_detail, register_user , dashboard , trends
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('records/', record_list_create),
    path('records/<int:pk>/', record_detail),
    path('register/', register_user),
    path('dashboard/', dashboard),
    path('trends/', trends),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]