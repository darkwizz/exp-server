from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def login(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def logout(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_eps(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_my_eps(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_ep(request, id):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_opportunities(request):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_opportunity(request, id):
    pass
