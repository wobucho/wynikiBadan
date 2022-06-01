from django.urls import path, include
from .views import badanieAPIView, registerMorfologiaKrwiAPIView, updateMorfologiaKrwiAPIView,\
    registerProbyWatroboweAPIView, updateProbyWatroboweAPIView, badaniaPacjentaAPIView, listaPacjentowAPIView, badaniaAPIView
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register('morfologia', morfolofiaKrwiAPIView, basename='morfologia')
#router.register('probywatr', probyWatroboweAPIView, basename='probywatr')


urlpatterns = [
    #path('', include(router.urls)),
    path('badanie/<int:id>/', badanieAPIView.as_view()),
    path('badania/', badaniaAPIView.as_view()),
    path('morfo/register/', registerMorfologiaKrwiAPIView.as_view()),
    path('morfo/<int:id>/', updateMorfologiaKrwiAPIView.as_view()),
    path('proby/register/', registerProbyWatroboweAPIView.as_view()),
    path('proby/<int:id>/', updateProbyWatroboweAPIView.as_view()),
    path('pacjent/<int:id>/', badaniaPacjentaAPIView.as_view()),
    path('lekarz/<int:id>/', listaPacjentowAPIView.as_view()),
]