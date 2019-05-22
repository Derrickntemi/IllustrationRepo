from django.urls import path
# import views from views.py
from .views import ListCreateArticlesView, ArticlesDetailView, LoginView, RegisterUsers, UsersDetailView


urlpatterns = [
    path('articles/', ListCreateArticlesView.as_view(),
         name="create-article"),
    path('articles/<int:pk>/', ArticlesDetailView.as_view(), name="article-info"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('users/<int:pk>/', UsersDetailView.as_view(), name="user-info")
    
]
