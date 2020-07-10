from rest_framework import serializers

from cdsso.contrib.countries.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
        description = "Countries and their identifiers"
