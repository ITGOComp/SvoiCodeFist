"""
Views for user service
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({'status': 'healthy', 'service': 'user_service'})


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    """Create user endpoint"""
    try:
        data = json.loads(request.body) if request.body else {}
        return JsonResponse({
            'message': 'User created successfully',
            'user_id': 1,
            'username': data.get('username', 'test_user')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["GET"])
def get_user(request, user_id):
    """Get user endpoint"""
    return JsonResponse({
        'user_id': user_id,
        'username': 'test_user',
        'email': 'test@example.com',
        'status': 'active'
    })


@require_http_methods(["GET"])
def list_users(request):
    """List users endpoint"""
    return JsonResponse({
        'users': [
            {'id': 1, 'username': 'admin', 'email': 'admin@example.com'},
            {'id': 2, 'username': 'user1', 'email': 'user1@example.com'}
        ],
        'count': 2
    })


@csrf_exempt
@require_http_methods(["POST"])
def authenticate_user(request):
    """Authenticate user endpoint"""
    try:
        data = json.loads(request.body) if request.body else {}
        username = data.get('username', '')
        password = data.get('password', '')
        
        if username and password:
            return JsonResponse({
                'message': 'Authentication successful',
                'token': 'jwt_token_here',
                'user': {
                    'id': 1,
                    'username': username,
                    'email': f'{username}@example.com'
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)