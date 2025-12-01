# chats/middleware.py

from datetime import datetime, time
from django.http import HttpResponseForbidden
import time as time_module  # to avoid conflict with datetime

# ---------------------------
# 1. Logging User Requests
# ---------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_text = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        
        with open("requests.log", "a") as f:
            f.write(log_text)

        return self.get_response(request)


# ---------------------------
# 2. Restrict Chat Access by Time
# ---------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start = time(18, 0)   # 6 PM
        allowed_end = time(21, 0)     # 9 PM

        if not (allowed_start <= current_time <= allowed_end):
            return HttpResponseForbidden("Chat allowed only between 6 PM and 9 PM.")

        return self.get_response(request)


# ---------------------------
# 3. Limit Messages per IP (Rate Limiting)
# ---------------------------
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # {ip_address: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            now = time_module.time()

            if ip not in self.requests:
                self.requests[ip] = []

            # Remove timestamps older than 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if now - t < 60]

            if len(self.requests[ip]) >= 5:
                return HttpResponseForbidden("Too many messages. Try again later.")

            self.requests[ip].append(now)

        return self.get_response(request)


# ---------------------------
# 4. Role Permission Middleware
# ---------------------------
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            role = getattr(user, "role", None)  # Assumes User model has 'role' field
            if role not in ["admin", "moderator"]:
                return HttpResponseForbidden("Access denied. Admins only.")
        else:
            return HttpResponseForbidden("Authentication required.")

        return self.get_response(request)
