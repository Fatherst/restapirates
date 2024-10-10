from rest_framework import serializers

class CurrencyInputSerializer(serializers.Serializer):
    cur_input = serializers.CharField(required=True)
    cur_output = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)

class CurrencyOutputSerializer(serializers.Serializer):
    result = serializers.FloatField()