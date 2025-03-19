from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer, UserSerializer, CustomTokenObtainPairSerializer
import json

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        # Try to handle the data in various formats
        try:
            # First check if we have parsed data already
            if hasattr(request, 'data') and request.data:
                if 'email' in request.data and 'password' in request.data:
                    data = request.data
                elif isinstance(request.data, dict) and len(request.data) == 1:
                    # Sometimes DRF puts the whole JSON string as a single key
                    possible_json = next(iter(request.data.keys()))
                    if possible_json.startswith('{') and possible_json.endswith('}'):
                        try:
                            data = json.loads(possible_json)
                        except:
                            data = request.data
                    else:
                        data = request.data
                else:
                    data = request.data
            else:
                # Try to parse raw body
                body = request.body.decode('utf-8')
                if body.startswith('{') and body.endswith('}'):
                    data = json.loads(body)
                else:
                    # This handles x-www-form-urlencoded content
                    import urllib.parse
                    parsed_body = urllib.parse.parse_qs(body)
                    data = {k: v[0] for k, v in parsed_body.items()}
        except Exception as e:
            print(f"Data parsing error: {e}")
            data = {}

        # Print debugging info
        print(f"Request content type: {request.content_type}")
        print(f"Parsed data: {data}")

        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        # Try to handle the data in various formats
        try:
            # First check if we have parsed data already
            if hasattr(request, 'data') and request.data:
                if 'email' in request.data and 'password' in request.data:
                    data = request.data
                elif isinstance(request.data, dict) and len(request.data) == 1:
                    # Sometimes DRF puts the whole JSON string as a single key
                    possible_json = next(iter(request.data.keys()))
                    if possible_json.startswith('{') and possible_json.endswith('}'):
                        try:
                            data = json.loads(possible_json)
                        except:
                            data = request.data
                    else:
                        data = request.data
                else:
                    data = request.data
            else:
                # Try to parse raw body
                body = request.body.decode('utf-8')
                if body.startswith('{') and body.endswith('}'):
                    data = json.loads(body)
                else:
                    # This handles x-www-form-urlencoded content
                    import urllib.parse
                    parsed_body = urllib.parse.parse_qs(body)
                    data = {k: v[0] for k, v in parsed_body.items()}
        except Exception as e:
            print(f"Data parsing error: {e}")
            data = {}

        # Print debugging info
        print(f"Request content type: {request.content_type}")
        print(f"Parsed data: {data}")

        # Use the token serializer
        serializer = CustomTokenObtainPairSerializer(data=data)
        if serializer.is_valid():
            return Response({
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)