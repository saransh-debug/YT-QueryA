from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view(['POST' , 'GET'])
def test(request):
    print((request.data))
    if not request.data:
        return Response({
            "status":200,
            "message":"test successful"
        })
    return Response(
        request.data
    )