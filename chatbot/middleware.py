from django.contrib.auth import logout

class ForceLogoutOnServerRestartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.has_logged_out = False  # Track if users have already been logged out

    def __call__(self, request):
        if not self.has_logged_out:
            logout(request)  # Logout user
            self.has_logged_out = True  # Prevent repeated logouts in a single session
        return self.get_response(request)
