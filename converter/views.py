from unicodedata import decimal

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
import requests
from .serializers import CurrencyInputSerializer, CurrencyOutputSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.conf import settings


@extend_schema(
    parameters=[
        OpenApiParameter(name='cur_input', description='Входная валюта', required=False, type=str),
        OpenApiParameter(name='cur_output', description='Выходная валюта', required=False, type=str),
        OpenApiParameter(name='amount', description='количество', required=False, type=float),
    ],
    responses={200: CurrencyOutputSerializer}
)
class ConverterView(APIView):
    def get_serializer(self, *args, **kwargs):
        return CurrencyOutputSerializer(*args, **kwargs)
    def get(self, request):
        filter_serializer = CurrencyInputSerializer(data=request.query_params)
        if filter_serializer.is_valid():
            try:
                data = filter_serializer.data
                params = {
                    'access_key': settings.RATE_URL,
                    'from': data['cur_input'],
                    'to': data['cur_output'],
                    'amount': data['amount']
                }
                response = requests.get("https://api.currencylayer.com/convert", params=params)
                response_data = response.json()
                serializer = CurrencyOutputSerializer({"result": round(response_data['result'], 2)})
                return Response(data=serializer.data)
            except Exception as err:
                return Response({"error": type(err)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
