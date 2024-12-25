# visualization/serializers.py
from rest_framework import serializers
from .models import RichPerson

class RichPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RichPerson
        fields = ['rank', 'name', 'total_net_worth', 'last_change', 'ytd_change', 'country_region', 'industry']
