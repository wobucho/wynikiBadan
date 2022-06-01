from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Pacjent, Lekarz, PacjentProfil, LekarzProfil, DiagnostaProfil
from .serializers import registerPacjentSerializer, registerLekarzSerializer, registerDiagnostaSerializer, loginSerializer,\
    pacjentProfilSerializer, pacjentProfilSerializerShort,lekarzProfilSerializer, diagnostaProfilSerializer, addPacjentSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist
from .permissions import LekarzPermission


# Create your views here.

class addPacjentAPIView(APIView):
    #authentication_classes = []
    permission_classes = [LekarzPermission, ]
    serializer_class = pacjentProfilSerializerShort

    def get_object(self, request):
        obj = request.user
        self.check_object_permissions(request, obj)
        return obj

    def post(self, request):
        user = self.get_object(request)
        pesel = request.data.get('pesel', None)
        try:
            pacjent = PacjentProfil.objects.get(pesel=pesel)
            type = user.type
            if type == User.Types.LEKARZ:
                serialized = self.serializer_class(pacjent)
                lekarz = LekarzProfil.objects.get(pk=user)
                lekarz.pacjenci.add(pacjent.user_id)
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response({'detail':"brak akcji"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'detail': "brak danych"}, status=status.HTTP_404_NOT_FOUND)

class removePacjentAPIView(APIView):
    #authentication_classes = []
    permission_classes = [LekarzPermission, ]
    serializer_class = pacjentProfilSerializer

    def get_object(self, request):
        obj = request.user
        self.check_object_permissions(request, obj)
        return obj

    def post(self, request):
        user = self.get_object(request)
        pesel = request.data.get('pesel', None)
        try:
            pacjent = PacjentProfil.objects.get(pesel=pesel)
            type = user.type
            if type == User.Types.LEKARZ:
                serialized = self.serializer_class(pacjent)
                lekarz = LekarzProfil.objects.get(pk=user)
                lekarz.pacjenci.remove(pacjent.user_id)
                return Response(serialized.data, status=status.HTTP_200_OK)
            return Response({'detail':"brak akcji"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'detail': "brak danych"}, status=status.HTTP_404_NOT_FOUND)


class userInformationAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        type = request.user.type
        if type == User.Types.PACJENT and PacjentProfil.objects.filter(pk=user):
            serialized = pacjentProfilSerializer(PacjentProfil.objects.get(pk=user))
            return Response(serialized.data, status=status.HTTP_200_OK)
        elif type == User.Types.LEKARZ and LekarzProfil.objects.filter(pk=user):
            serialized = lekarzProfilSerializer(LekarzProfil.objects.get(pk=user))
            return Response(serialized.data, status=status.HTTP_200_OK)
        elif type == User.Types.DIAGNOSTA and DiagnostaProfil.objects.filter(pk=user):
            serialized = diagnostaProfilSerializer(DiagnostaProfil.objects.get(pk=user))
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response({'detail':"brak danych"}, status=status.HTTP_404_NOT_FOUND)


class registerPacjentAPIView(APIView):
    authentication_classes = []
    serializer_class = registerPacjentSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class registerLekarzAPIView(APIView):
    authentication_classes = []
    serializer_class = registerLekarzSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class registerDiagnostaAPIView(APIView):
    authentication_classes = []
    serializer_class = registerDiagnostaSerializer

    def post(self, request):
        serialized = self.serializer_class(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class loginAPIView(APIView):
    authentication_classes = []
    serializer_class = loginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if user:
            serialized = self.serializer_class(user)

            return Response(serialized.data, status.HTTP_200_OK)
        return Response({'detail':"Nieprawidłowy login lub hasło."}, status=status.HTTP_401_UNAUTHORIZED)