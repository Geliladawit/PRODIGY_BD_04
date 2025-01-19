from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import time

class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        start_time = time.time()
        cache_key = 'users'
        users = cache.get(cache_key)

        if not users:
            users = User.objects.all() 
            serializer = UserSerializer(users, many=True)  
            cache.set(cache_key, serializer.data, timeout=60 * 15)  
        else:
            serializer = users 

        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")
        return Response(serializer, status=status.HTTP_200_OK)  

class UserDetailView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        start_time = time.time()
        cache_key = f"user_{user_id}"
        user = cache.get(cache_key)

        if not user:
            try:
                user = User.objects.get(id=user_id)  
                serializer = UserSerializer(user)  
                cache.set(cache_key, serializer.data, timeout=60 * 15)  
            except User.DoesNotExist:
                return Response({"error": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        end_time = time.time()
        print(f"Response time: {end_time - start_time} seconds")
        return Response(serializer.data, status=status.HTTP_200_OK)  