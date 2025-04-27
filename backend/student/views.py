from django.shortcuts import render
import json
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Student

class ValidateTokenView(APIView):
    """
    API view for validating OTPless tokens and directing students.
    """
    
    def post(self, request):
        try:
            token = request.data.get('token')
            if not token:
                return Response(
                    {'success': False, 'message': 'Token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            validation_url = 'https://user-auth.otpless.app/auth/v1/validate/token'
            
            headers = {
                'Content-Type': 'application/json',
                'clientId': settings.OTPLESS_CLIENT_ID,
                'clientSecret': settings.OTPLESS_CLIENT_SECRET
            }
            
            data = {
                'token': token
            }
            
            try:
                response = requests.post(
                    validation_url,
                    headers=headers,
                    data=json.dumps(data),
                    timeout=10
                )
                
                if response.status_code == 200:
                    otpless_data = response.json()
                    user_id = otpless_data.get('userId')
                    user_exists = User.objects.filter(user_id=user_id).exists()
                    identities = otpless_data.get('identities', [])
                    identity = identities[0] if identities else {}
                    identity_type = identity.get('identityType', '')
                    identity_value = identity.get('identityValue', '')
                    name = identity.get('name', '')
                    
                    if not user_exists:
                        user = User.objects.create(
                            user_id=user_id,
                            identity_type=identity_type,
                            identity_value=identity_value,
                            name=name,
                            user_type='student'
                        )
                        Student.objects.create(user=user)
                        is_new_user = True
                    else:
                        user = User.objects.get(user_id=user_id)
                        user.name = name or user.name
                        user.identity_type = identity_type or user.identity_type
                        user.identity_value = identity_value or user.identity_value
                        user.save()
                        # Check if profile is incomplete (e.g., gender or age is null)
                        is_new_user = not (user.gender and user.age)
                    
                    dashboard_route = 'StudentDashboard'
                    
                    user_data = {
                        'success': True,
                        'message': 'Token verified successfully',
                        'user_id': user_id,
                        'name': user.name,
                        'identity_type': user.identity_type,
                        'identity_value': user.identity_value,
                        'user_type': user.user_type,
                        'dashboard_route': dashboard_route,
                        'is_new_user': is_new_user,
                        'identities': otpless_data.get('identities', []),
                        'timestamp': otpless_data.get('timestamp')
                    }
                    
                    return Response(user_data, status=status.HTTP_200_OK)
                else:
                    error_message = f"OTPless validation failed with status code: {response.status_code}"
                    try:
                        error_data = response.json()
                        error_message = error_data.get('message', error_message)
                    except:
                        pass
                    
                    return Response(
                        {'success': False, 'message': error_message},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except requests.exceptions.RequestException as e:
                return Response(
                    {'success': False, 'message': f'Error connecting to OTPless: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateProfileView(APIView):
    """
    API view for updating student profile details.
    """
    def post(self, request):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'))
            user.name = request.data.get('name', user.name)
            user.gender = request.data.get('gender', user.gender)
            user.age = request.data.get('age', user.age)
            user.save()
            
            student = Student.objects.get(user=user)
            student.grade = request.data.get('grade', student.grade)
            student.school = request.data.get('school', student.school)
            student.save()
            
            return Response(
                {'success': True, 'message': 'Profile updated successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Error updating profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetProfileView(APIView):
    """
    API view for retrieving student profile details.
    """
    def post(self, request):
        try:
            user = User.objects.get(user_id=request.data.get('user_id'))
            student = Student.objects.get(user=user)
            profile_data = {
                'name': user.name,
                'gender': user.gender,
                'age': user.age,
                'grade': student.grade,
                'school': student.school,
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Error retrieving profile: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )