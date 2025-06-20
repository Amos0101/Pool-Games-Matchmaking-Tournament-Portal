from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if session has expired
            last_activity = request.session.get('last_activity')

            if last_activity:
                # Convert string back to datetime if it exists
                if isinstance(last_activity, str):
                    from django.utils.dateparse import parse_datetime
                    last_activity = parse_datetime(last_activity)

                # Check if session has expired (30 minutes of inactivity)
                if timezone.now() - last_activity > timedelta(minutes=30):
                    logout(request)
                    messages.warning(request, 'Your session has expired due to inactivity. Please log in again.')
                    return redirect('accounts:login')

            # Update last activity time
            request.session['last_activity'] = timezone.now().isoformat()

            # Extend session expiry on activity
            request.session.set_expiry(1800)  # 30 minutes from now

        response = self.get_response(request)
        return response
