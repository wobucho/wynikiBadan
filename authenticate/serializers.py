from rest_framework import serializers
from .models import User, Pacjent, Lekarz, Diagnosta, PacjentProfil, LekarzProfil, DiagnostaProfil


class addPacjentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pacjent
        fields = ('pesel')


class pacjentProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacjentProfil
        fields = ('user', 'imie', 'nazwisko', 'pesel', 'telefon')

class pacjentProfilSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = PacjentProfil
        fields = ('imie', 'nazwisko', 'pesel', 'telefon')


class lekarzProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = LekarzProfil
        fields = ('imie', 'nazwisko', 'pwz', 'telefon')

class diagnostaProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnostaProfil
        fields = ('imie', 'nazwisko', 'telefon')

class registerPacjentSerializer(serializers.ModelSerializer):
    profilP = pacjentProfilSerializerShort(required=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = Pacjent
        fields = ('email', 'password', 'profilP')

    def create(self, validated_data):
        pacjent = Pacjent.objects.create_user(email=validated_data.pop('email'), password=validated_data.pop('password'))
        profil_data = validated_data.pop('profilP')
        profil = PacjentProfil.objects.create(
            user=pacjent,
            pesel=profil_data['pesel'],
            imie=profil_data['imie'],
            nazwisko=profil_data['nazwisko'],
            telefon=profil_data['telefon']
        )
        return pacjent


class registerLekarzSerializer(serializers.ModelSerializer):
    profilL = lekarzProfilSerializer(required=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = Lekarz
        fields = ('email', 'password', 'profilL')

    def create(self, validated_data):
        lekarz = Lekarz.objects.create_user(email=validated_data.pop('email'), password=validated_data.pop('password'))
        profil_data = validated_data.pop('profilL')
        profil = LekarzProfil.objects.create(
            user=lekarz,
            pwz=profil_data['pwz'],
            imie=profil_data['imie'],
            nazwisko=profil_data['nazwisko'],
            telefon=profil_data['telefon'],
        )
        #profil.pacjenci.set(profil_data['pacjenci'])
        return lekarz

class registerDiagnostaSerializer(serializers.ModelSerializer):
    profilD = diagnostaProfilSerializer(required=True)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = Diagnosta
        fields = ('email', 'password', 'profilD')

    def create(self, validated_data):
        diagnosta = Diagnosta.objects.create_user(email=validated_data.pop('email'), password=validated_data.pop('password'))
        profil_data = validated_data.pop('profilD')
        profil = DiagnostaProfil.objects.create(
            user=diagnosta,
            imie=profil_data['imie'],
            nazwisko=profil_data['nazwisko'],
            telefon=profil_data['telefon'],
        )
        return diagnosta


class loginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'type', 'token')

        read_only_fields = ['token', 'type']