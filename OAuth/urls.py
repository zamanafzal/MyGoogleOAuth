from django.urls import path

from OAuth.views import UserGoogleAuthView

urlpatterns = [
    path('google-auth/', UserGoogleAuthView.as_view()),
]
