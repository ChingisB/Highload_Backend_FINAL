from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.META.get('CSRF_COOKIE'):
            return JsonResponse({'error': 'CSRF token missing'}, status=403)

        if request.path.startswith('/api/auth/') and request.method in ['POST', 'PUT', 'DELETE']:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=401)

