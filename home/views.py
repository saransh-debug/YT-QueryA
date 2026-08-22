from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import parse_qs , urlparse
from .RAG import Rag
from .models import Main_Model
from django.contrib.auth.models import User
from .serializers import Main_serializer
# Create your views here.


@api_view(['POST' , 'GET'])
def test(request):
    link = request.data['link'] if request.data else None
    query = request.data['query'] if request.data else None
    
    if request.user.is_authenticated:
        user = request.user 
    else:
        user = User.objects.filter(is_superuser=True).first()
    res = Rag(link , query)
    Main_Model.objects.create(
        user=user , 
        link=link , 
        query = query ,
        response=res
    )
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

@api_view(['GET'])
def Db_details(request):
    queryset = Main_Model.objects.all()
    serailizer = Main_serializer(queryset , many=True)


    return Response({
        "data":serailizer.data
    })
