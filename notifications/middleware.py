from .models import Notification

class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.notifications = Notification.objects.filter(
                user=request.user,
                is_read=False
            )
        else:
            request.notifications = []
        
        response = self.get_response(request)
        return response