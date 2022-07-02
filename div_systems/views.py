from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

# Create your views here.

# custom decroator for special permission on class based views functions


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class UserDetailsView(APIView):
    def get_object(self, pk):
        try:
            return get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            raise Http404

    @method_permission_classes((IsAuthenticated,))
    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(data={'id': user.id, **serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    response = {}
    user_qs = get_user_model().objects.filter(
        phone_number=request.data['phone_number'])
    if user_qs.exists():
        user = user_qs.first()
        if user.check_password(request.data['password']):
            refresh_token = RefreshToken.for_user(user)
            response = {
                'data': {
                    'refresh_token': str(refresh_token),
                    'access_token': str(refresh_token.access_token)
                },
                'status': status.HTTP_202_ACCEPTED
            }
        else:
            response = {
                'data': {'error': 'incorrect password check password and try again'},
                'status': status.HTTP_401_UNAUTHORIZED
            }
    else:
        response = {
            "data": {'error': f"user with phone number {request.data['phone_number']} isn't in our database, check he number and try again, note that the number should begain with + following by country dial code"},
            'status': status.HTTP_404_NOT_FOUND
        }
    return Response(data=response['data'], status=response['status'])
