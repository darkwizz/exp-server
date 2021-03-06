# Create your views here.
import requests
from django.contrib.auth import login as auth_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import logout as auth_logout
from exp_rest.api.v1.serializers import AuthSerializer


BASE_URL = 'https://gis-api.aiesec.org/v2/'
API_REQUESTS = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
}


@api_view(['POST'])
def login(request):
    if not request.user.is_anonymous():
        auth_logout(request)
    serial = AuthSerializer(data=request.data)
    if serial.is_valid():
        token = serial.login()
        if not token:
            return Response({'detail': 'Failed to login; incorrect email or password'}, status.HTTP_400_BAD_REQUEST)
        # auth_login(request, request.user)
        return Response({'token': token}, status.HTTP_200_OK)
    return Response({'detail': 'Invalid login data'}, status.HTTP_400_BAD_REQUEST)


"""
EXP logout doesn't work correctly. I can use two tokens at same time
and one of them was used to sign_out from experience.org
"""


@api_view(['POST'])
def logout(request):
    detail = {
        'detail': 'Successfully logged out',
    }
    response = Response(detail, status.HTTP_200_OK)
    if request.user.is_anonymous():
        return response
    # auth_logout(request)
    return response


def get_api_request_result(url, data, method):
    headers = {}
    if method != 'GET':
        headers['Content-type'] = 'application/json'
    response = API_REQUESTS[method](BASE_URL + url, data=data, headers=headers)
    if response.status_code >= 400:
        return [None, response.status_code, response.content]
    result = response.json()
    return [result]


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def get_eps(request, token):
    if not token:
        return Response({'detail': 'No access to do this'}, status.HTTP_401_UNAUTHORIZED)
    result = get_api_request_result('people', {'access_token': token}, 'GET')
    if len(result) > 1:
        return Response({'detail': result[2]}, status=result[1])
    return Response(result[0], status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def get_my_eps(request, token):
    if not token:
        return Response({'detail': 'No access to do this'}, status.HTTP_401_UNAUTHORIZED)
    result = get_api_request_result('people/my', {'access_token': token}, 'GET')
    if len(result) > 1:
        return Response({'detail': result[2]}, status=result[1])
    return Response(result[0], status.HTTP_200_OK)


@api_view(['GET'])
def get_ep(request, id, token):
    if not token:
        return Response({'detail': 'No access to do this'}, status.HTTP_401_UNAUTHORIZED)
    result = get_api_request_result('people/' + id, {'access_token': token}, 'GET')
    if len(result) > 1:
        return Response({'detail': result[2]}, status=result[1])
    return Response(result[0], status.HTTP_200_OK)


@api_view(['GET'])
def get_opportunities(request, token):
    if not token:
        return Response({'detail': 'No access to do this'}, status.HTTP_401_UNAUTHORIZED)
    result = get_api_request_result('opportunities', {'access_token': token}, 'GET')
    if len(result) > 1:
        return Response({'detail': result[2]}, status=result[1])
    return Response(result[0], status.HTTP_200_OK)


@api_view(['GET'])
def get_opportunity(request, id, token):
    if not token:
        return Response({'detail': 'No access to do this'}, status.HTTP_401_UNAUTHORIZED)
    result = get_api_request_result('opportunities/' + id, {'access_token': token}, 'GET')
    if len(result) > 1:
        return Response({'detail': result[2]}, status=result[1])
    return Response(result[0], status.HTTP_200_OK)
