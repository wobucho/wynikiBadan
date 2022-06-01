from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import badania, morfologiaKrwi, probyWatrobowe
from .serializers import badaniaSerializer, morfologiaKrwiSerializer, probyWatroboweSerializer, \
    registerMorfologiaKrwiSerializer, updateMorfologiaKrwiSerializer, registerProbyWatroboweSerializer, updateProbyWatroboweSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth import authenticate
from .permissions import BadaniePermission, LaborantPermission, BadaniaPacjentaPermission, PacjenciPermission, DetailBadaniePermission
from rest_framework import exceptions
from authenticate.models import PacjentProfil, LekarzProfil
from django.core.exceptions import ObjectDoesNotExist
from authenticate.serializers import pacjentProfilSerializer


# Create your views here.

class listaPacjentowAPIView(APIView):
    # authentication_classes = []
    permission_classes = [PacjenciPermission, ]
    serializer_class = pacjentProfilSerializer
    queryset = LekarzProfil.objects.all()

    lookup_field = 'id'

    def get_object(self, id):
        obj = LekarzProfil.objects.get(pk=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, id):
        try:
            lekarz = self.get_object(id)
            pacjenci_lekarza = lekarz.pacjenci.all()
            serialized = self.serializer_class(pacjenci_lekarza, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except exceptions.AuthenticationFailed:
            return Response({'detail': "odmowa dostępu"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'detail':"brak danych"}, status=status.HTTP_404_NOT_FOUND)

class badaniaPacjentaAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # authentication_classes = []
    permission_classes = [BadaniaPacjentaPermission, ]
    serializer_class = badaniaSerializer
    queryset = badania.objects.all()

    lookup_field = 'id'

    def get_object(self, id):
        obj = PacjentProfil.objects.get(pk=id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, id):
        try:
            pacjent = self.get_object(id)
            badania_pacjenta = badania.objects.filter(pacjent=pacjent)
            serialized = badaniaSerializer(badania_pacjenta, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except exceptions.AuthenticationFailed:
            return Response({'detail': "odmowa dostępu"}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'detail':"brak danych"}, status=status.HTTP_404_NOT_FOUND)


class badanieAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    # authentication_classes = []
    permission_classes = [BadaniePermission, ]
    serializer_class = badaniaSerializer
    queryset = badania.objects.all()

    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id)

class badaniaAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                                    mixins.CreateModelMixin):
    # authentication_classes = []
    permission_classes = [LaborantPermission, ]
    serializer_class = badaniaSerializer
    queryset = badania.objects.all()

    def get(self, request):
        return self.list(request)


class registerMorfologiaKrwiAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                                    mixins.CreateModelMixin):
    #authentication_classes = []
    permission_classes = [LaborantPermission, ]
    serializer_class = registerMorfologiaKrwiSerializer
    queryset = morfologiaKrwi.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class updateMorfologiaKrwiAPIView(APIView):
    #authentication_classes = []
    permission_classes = [DetailBadaniePermission, ]
    serializer_class = registerMorfologiaKrwiSerializer
    queryset = morfologiaKrwi.objects.all()

    lookup_field = 'id'

    def get_object(self, id):
        obj = morfologiaKrwi.objects.get(pk=id)
        return obj

    def get(self, request, id):
        try:
            morfo = self.get_object(id)
        except:
            return Response({'detail': "brak danych"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, morfo)
        serialized = updateMorfologiaKrwiSerializer(morfo)
        return Response(serialized.data)


    def put(self, request, id):
        try:
            morfo = self.get_object(id)
        except:
            return Response({'detail': "istnieje badanie innego typu o tym numerze"}, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(self.request, morfo)
        serialized = updateMorfologiaKrwiSerializer(morfo, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class registerProbyWatroboweAPIView(generics.GenericAPIView, mixins.ListModelMixin,
                                    mixins.CreateModelMixin):
    #authentication_classes = []
    permission_classes = [LaborantPermission, ]
    serializer_class = registerProbyWatroboweSerializer
    queryset = probyWatrobowe.objects.all()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)



class updateProbyWatroboweAPIView(APIView):
    #authentication_classes = []
    permission_classes = [DetailBadaniePermission, ]
    serializer_class = registerProbyWatroboweSerializer
    queryset = probyWatrobowe.objects.all()

    lookup_field = 'id'

    def get_object(self, id):
        return probyWatrobowe.objects.get(pk=id)

    def get(self, request, id):
        try:
            proby = self.get_object(id)
        except:
            return Response({'detail': "brak danych"}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(self.request, proby)
        serialized = updateProbyWatroboweSerializer(proby)
        return Response(serialized.data)


    def put(self, request, id):
        try:
            proby = self.get_object(id)
        except:
            return Response({'detail': "istnieje badanie innego typu o tym numerze"}, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(self.request, proby)
        serialized = updateProbyWatroboweSerializer(proby, data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

