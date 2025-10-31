"""
Audit logging middleware
"""
import json
from django.utils import timezone
from .models import AuditLog


class AuditLogMiddleware:
    """Middleware to log user actions"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Actions to log (exclude safe methods unless they modify data)
        self.log_actions = ['POST', 'PUT', 'PATCH', 'DELETE']
        
        # Paths to exclude
        self.excluded_paths = [
            '/static/',
            '/media/',
            '/api/auth/login/',
            '/api/auth/logout/',
            '/api/auth/refresh/',
            '/admin/jsi18n/',
        ]
    
    def __call__(self, request):
        # Skip logging for excluded paths
        if any(request.path.startswith(path) for path in self.excluded_paths):
            return self.get_response(request)
        
        # Track request start time
        start_time = timezone.now()
        
        response = self.get_response(request)
        
        # Log important actions
        if request.method in self.log_actions and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                # Determine entity type and ID from URL
                entity_type, entity_id = self._extract_entity_info(request.path)
                
                # Get action details
                action_details = {
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_ms': (timezone.now() - start_time).total_seconds() * 1000,
                }
                
                # Include request body for POST/PUT/PATCH (be careful with sensitive data)
                if request.method in ['POST', 'PUT', 'PATCH'] and hasattr(request, 'body'):
                    try:
                        body = json.loads(request.body.decode('utf-8')) if request.body else {}
                        # Exclude sensitive fields
                        sanitized_body = {k: v for k, v in body.items() 
                                        if k not in ['password', 'token', 'secret', 'key']}
                        action_details['request_body'] = sanitized_body
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass
                
                # Create audit log entry
                AuditLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    action_type=self._determine_action_type(request.method, request.path),
                    entity_type=entity_type,
                    entity_id=entity_id,
                    action_details=action_details,
                    ip_address=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                )
            except Exception as e:
                # Don't fail the request if logging fails
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Audit logging failed: {str(e)}")
        
        return response
    
    def _extract_entity_info(self, path):
        """Extract entity type and ID from URL path"""
        # Parse URL pattern: /api/{entity}/{id}/
        parts = path.strip('/').split('/')
        
        if len(parts) >= 3 and parts[0] == 'api':
            entity_type = parts[1]
            entity_id = parts[2] if len(parts) > 2 else None
            return entity_type, entity_id
        
        return 'unknown', None
    
    def _determine_action_type(self, method, path):
        """Determine action type from HTTP method and path"""
        if method == 'POST':
            if 'verify' in path:
                return 'verify'
            elif 'assign' in path:
                return 'assign'
            elif 'close' in path:
                return 'close'
            return 'create'
        elif method == 'PUT' or method == 'PATCH':
            return 'update'
        elif method == 'DELETE':
            return 'delete'
        return 'read'
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
