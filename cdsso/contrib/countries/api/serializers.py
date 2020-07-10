from rest_framework import serializers

from cdsso.contrib.countries.models import Country


class CountrySerializer(serializers.ModelSerializer):
    numeric_code = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = Country
        fields = "__all__"
        description = "Countries and their identifiers"
    
    def get_numeric_code(self, obj: Country):
        """Returns the 3-digit numeric code."""
        return obj.get_numeric_code()
