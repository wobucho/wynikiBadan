from django.urls import path, include
from .views import registerPacjentAPIView, registerLekarzAPIView, loginAPIView, userInformationAPIView, addPacjentAPIView, removePacjentAPIView, registerDiagnostaAPIView
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register('badania', badaniaAPIView, basename='badania')
#router.register('morfologia', morfolofiaKrwiAPIView, basename='morfologia')
#router.register('proby', probyWatroboweAPIView, basename='proby')


urlpatterns = [
    #path('wynikiBadan2/', include(router.urls)),
    path('register/pacjent/', registerPacjentAPIView.as_view()),
    path('register/lekarz/', registerLekarzAPIView.as_view()),
    path('register/diagnosta/', registerDiagnostaAPIView.as_view()),
    path('login/', loginAPIView.as_view()),
    path('user/', userInformationAPIView.as_view()),
    path('dodajpacjenta/', addPacjentAPIView.as_view()),
    path('usunpacjenta/', removePacjentAPIView.as_view()),
]