# Security Measures

## Overview

This document outlines the security measures implemented for securing user login and registration in the Django application.

## Security Middleware

The `SecurityMiddleware` is designed to enforce security measures for requests to sensitive endpoints.

### Middleware Implementation

```python
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.META.get('CSRF_COOKIE'):
            return JsonResponse({'error': 'CSRF token missing'}, status=403)

        if request.path.startswith('/api/auth/') and request.method in ['POST', 'PUT', 'DELETE']:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)
```

## Secure User Login (POST /api/auth/login/)
The login view handles user authentication using a username and password.

### Implementation

```python
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
```

## Secure User Registration (POST /api/auth/register/)
The registration view handles user creation with username, password, and email.

### Implementation

```python
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return JsonResponse({'message': 'User registered successfully'})
```

## Conclusion

This document outlines the implementation of security measures for securing user login and registration in the Django application using a custom security middleware and API views.
This document covers both the middleware and API views for ensuring secure login and registration in your Django application.