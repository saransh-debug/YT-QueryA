from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import parse_qs , urlparse
from .RAG import Rag
# Create your views here.


@api_view(['POST' , 'GET'])
def test(request):
    link = request.data['link']
    query = request.data['query']
    print(link , query)
    res = Rag(link , query)

    if not res:
        return Response({
            "status":403,
            "message":"Error"
        })
    return Response(
        {
            "AI_response": res
        }
    )