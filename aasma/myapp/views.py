from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

import os

import fitz
from django.http import HttpResponse
from requests import session
from rest_framework import status
from weasel.util import download_file

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import uuid
import bcrypt
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import random
from django.core.mail import send_mail
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import AuthenticationFailed

from .models import User, OTP, Token, Employee
from .pagination import UserPagination
from .permissions import IsAuthenticatedUser
from .serializers import RegisterSerializer, OTPSerializer, UserSerializer, UserProfileSerializer, UserDetailSerializer


class Loginuser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from .serializers import LoginSerializer
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username, password)  # Debugging output
            try:
                # Authenticate user
                user = Employee.objects.get(username=username)

                # Verify password
                if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    raise AuthenticationFailed('Invalid credentials')

                # Check if the user is verified
                if not user.isverified:
                    # Resend OTP
                    otp_code = str(random.randint(100000, 999999))
                    OTP.objects.create(email=user.email, otp=otp_code)

                    # Send OTP via email
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp_code}. It will expire in 5 minutes.',
                        'Dungeon0559@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )

                    return Response({
                        'message': 'Your account is not verified. A new OTP has been sent to your email.',
                        'email': user.email
                    }, status=401)

                # Generate a new token key
                token_key = str(uuid.uuid4())

                # Try to find an existing token for the user
                token = Token.objects(employee=user).first()

                if token:
                    # Update the existing token
                    token.key = token_key
                    token.expires_at = datetime.utcnow() + timedelta(days=7)  # Reset expiration to 7 days
                    token.save()
                else:
                    # Create a new token
                    token = Token(
                        employee=user,
                        key=token_key,
                        expires_at=datetime.utcnow() + timedelta(days=7)  # Set expiration to 7 days
                    )
                    token.save()

                # Set the token in the response headers
                response = Response({
                    'message': 'Login successful',
                }, status=200)
                response['Authorization'] = f'Token {token.key}'
                return response

            except Employee.DoesNotExist:
                raise AuthenticationFailed('Invalid credentials')
        else:
            return Response(serializer.errors, status=400)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        # Retrieve employee_id from request data
        employee_id = request.data.get('employee_id')

        # Debugging: print received employee_id
        print("Received employee_id:", employee_id)

        if not employee_id:
            return Response({'error': 'Employee ID not provided'}, status=400)

        try:
            # Fetch user based on employee_id
            user = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)

        if user.isverified:
            return Response({'message': 'User is already verified'}, status=400)

        # Generate OTP
        otp_code = str(random.randint(100000, 999999))
        OTP.objects(email=user.email).delete()  # Assuming OTP is associated with email
        OTP.objects.create(email=user.email, otp=otp_code)

        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}. It will expire in 5 minutes.',
            'Dungeon0559@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'A new OTP has been sent to your email'}, status=200)



class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        data = serializer.validated_data

        if Employee.objects(email=data['email']).first() or Employee.objects(contact_number=data['contact_number']).first():
            return Response({'error': 'User with this email or contact number already exists'}, status=409)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Storing user data in session
        # request.session['email'] = data['email']
        # request.session['username'] = data['username']  # Ensure username is stored
        #
        # # Save the session data to MongoDB
        # request.session.save()

        # Set a session cookie

        user = Employee(
            email=data['email'],
            contact_number=data['contact_number'],
            username=data['username'],
            password=hashed_password.decode('utf-8'),
            isverified=False
        )
        user.save()
        # Optional: Set a custom cookie if needed
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(email=data['email'], otp=otp_code)

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}. It will expire in 5 minutes.',
            'Dungeon0559@gmail.com',
            [data['email']],
            fail_silently=False,
        )

        return Response({
            'message': 'Registration successful. Please verify your email with the OTP sent to you.',
            'user_id': str(user.id)  # Assuming user.id is an ObjectId and needs to be converted to a string
        }, status=201)
class VerifyOTPAndRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid OTP or email'}, status=400)

        data = serializer.validated_data
        otp_record = OTP.objects(email=data['email'], otp=data['otp']).first()

        if not otp_record or otp_record.is_expired():
            return Response({'error': 'Invalid or expired OTP'}, status=400)

        # Remove the OTP after successful verification
        OTP.objects(email=data['email']).delete()

        # Mark the user as verified
        user = Employee.objects(email=data['email']).first()
        if not user:
            return Response({'error': 'User not found'}, status=404)

        user.isverified = True
        user.save()

        return Response({'message': 'Email verified successfully. You can now log in.'}, status=200)


class AddUser(APIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Extract email and username from the request data
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')

            # Check if a user with the same email or username already exists
            if User.objects(email=email).count() > 0:
                return Response({
                    'error': 'User with this email already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)

            if User.objects(username=username).count() > 0:
                return Response({
                    'error': 'User with this username already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # If no existing user found, create a new user
            user = serializer.save()
            return Response({
                'id': str(user.id),  # Convert ObjectId to string
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserListView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         paginator = UserPagination()
#         queryset = User.objects.all()
#
#         page = paginator.paginate_queryset(queryset, request)
#         if page is not None:
#             serializer = UserProfileSerializer(page, many=True)
#             # print("Paginated serialized data:", serializer.data)
#             return paginator.get_paginated_response(serializer.data)
#
#         serializer = UserProfileSerializer(queryset, many=True)
#         # print("Full serialized data:", serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from django.db.models import Q
from django.urls import reverse

from mongoengine.queryset.visitor import Q as MongoQ

class UserListView(APIView):
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        page_number = int(request.GET.get('page', 1))

        # Filter users based on search query using MongoEngine's Q objects
        if search_query:
            users = User.objects.filter(
                MongoQ(full_name__icontains=search_query) |
                MongoQ(username__icontains=search_query) |
                MongoQ(email__icontains=search_query)
            )
        else:
            users = User.objects.all()

        # Paginate the queryset
        paginator = Paginator(users, 9)  # 9 users per page
        page = paginator.get_page(page_number)

        serializer = UserProfileSerializer(page.object_list, many=True)

        # Build absolute URIs for pagination
        def build_page_url(page_num):
            return request.build_absolute_uri(f'/api/get_users/?page={page_num}&search={search_query}')

        response_data = {
            'count': paginator.count,
            'next': page.has_next() and build_page_url(page.next_page_number()),
            'previous': page.has_previous() and build_page_url(page.previous_page_number()),
            'results': serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)




from bson import ObjectId
from mongoengine import DoesNotExist


class UserDetailView(APIView):
    permission_classes = [IsAuthenticatedUser]
    def get(self, request, user_id, *args, **kwargs):
        print(f"Received user_id: {user_id}")
        try:
            object_id = ObjectId(user_id)
            print(f"Converted to ObjectId: {object_id}")
            user = User.objects.get(id=object_id)
            print(f"User found: {user.username}")
        except (DoesNotExist, ValueError, TypeError) as e:
            print(f"Error: {e}")
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)