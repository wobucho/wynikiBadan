from rest_framework import serializers
from .models import badania, morfologiaKrwi, probyWatrobowe
from authenticate.models import PacjentProfil
from django.utils.translation import gettext_lazy as _


class badaniaSerializer(serializers.ModelSerializer):
    pacjent = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='pesel',
        queryset=PacjentProfil.objects.all()
    )

    class Meta:
        model = badania
        fields = ('id', 'dataBadania', 'typBadania', 'pacjent')


class badaniaNoTypeSerializer(serializers.ModelSerializer):
    pacjent = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='pesel',
        queryset=PacjentProfil.objects.all()
    )

    class Meta:
        model = badania
        fields = ('id', 'dataBadania', 'pacjent')


class morfologiaKrwiSerializer(serializers.ModelSerializer):
    class Meta:
        model = morfologiaKrwi
        fields = '__all__'


class probyWatroboweSerializer(serializers.ModelSerializer):
    class Meta:
        model = probyWatrobowe
        fields = '__all__'


class registerMorfologiaKrwiSerializer(serializers.ModelSerializer):
    badanie = badaniaNoTypeSerializer(required=True)

    class Meta:
        model = morfologiaKrwi
        fields = ('badanie', 'HGB', 'HCT', 'WBC', 'RBC', 'PLT', 'CRP')

    def create(self, validated_data):
        badanie_data = validated_data.pop('badanie')
        badanie = badania.objects.create(dataBadania=badanie_data['dataBadania'], typBadania=badania.MORFOLOGIAKRWI,
                                         pacjent=badanie_data['pacjent'])
        morfoK = morfologiaKrwi.objects.create(
            badanie=badanie,
            HGB=validated_data['HGB'],
            HCT=validated_data['HCT'],
            WBC=validated_data['WBC'],
            RBC=validated_data['RBC'],
            PLT=validated_data['PLT'],
            CRP=validated_data['CRP'],
        )
        return morfoK


class updateMorfologiaKrwiSerializer(serializers.ModelSerializer):
    badanie = badaniaNoTypeSerializer(required=True)

    class Meta:
        model = morfologiaKrwi
        fields = ('badanie', 'HGB', 'HCT', 'WBC', 'RBC', 'PLT', 'CRP')

    def update(self, instance, validated_data):
        badanie_data = validated_data.pop('badanie')
        badanie_id = instance.badanie.id
        badanie = badania.objects.get(pk=badanie_id)
        badanie.dataBadania = badanie_data.get('dataBadania')
        badanie.typBadania = badania.MORFOLOGIAKRWI
        badanie.pacjent = badanie_data.get('pacjent')
        badanie.save()

        instance.badanie = badanie
        instance.HGB = validated_data.get('HGB')
        instance.HCT = validated_data.get('HCT')
        instance.WBC = validated_data.get('WBC')
        instance.RBC = validated_data.get('RBC')
        instance.PLT = validated_data.get('PLT')
        instance.CRP = validated_data.get('CRP')
        instance.save()
        return instance


class registerProbyWatroboweSerializer(serializers.ModelSerializer):
    badanie = badaniaNoTypeSerializer(required=True)

    class Meta:
        model = probyWatrobowe
        fields = ('badanie', 'ALT', 'AST', 'ALP', 'BIL', 'GGTP')

    def create(self, validated_data):
        badanie_data = validated_data.pop('badanie')
        badanie = badania.objects.create(dataBadania=badanie_data['dataBadania'], typBadania=badania.PROBYWATROBOWE,
                                         pacjent=badanie_data['pacjent'])
        probyW = probyWatrobowe.objects.create(
            badanie=badanie,
            ALT=validated_data['ALT'],
            AST=validated_data['AST'],
            ALP=validated_data['ALP'],
            BIL=validated_data['BIL'],
            GGTP=validated_data['GGTP'],
        )
        return probyW


class updateProbyWatroboweSerializer(serializers.ModelSerializer):
    badanie = badaniaNoTypeSerializer(required=True)

    class Meta:
        model = probyWatrobowe
        fields = ('badanie', 'ALT', 'AST', 'ALP', 'BIL', 'GGTP')

    def update(self, instance, validated_data):
        badanie_data = validated_data.pop('badanie')
        badanie_id = instance.badanie.id
        badanie = badania.objects.get(pk=badanie_id)
        badanie.dataBadania = badanie_data.get('dataBadania')
        badanie.typBadania = badania.PROBYWATROBOWE
        badanie.pacjent = badanie_data.get('pacjent')
        badanie.save()

        instance.badanie = badanie
        instance.ALT = validated_data.get('ALT')
        instance.AST = validated_data.get('AST')
        instance.ALP = validated_data.get('ALP')
        instance.BIL = validated_data.get('BIL')
        instance.GGTP = validated_data.get('GGTP')
        instance.save()
        return instance
