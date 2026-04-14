import time
import threading
from functools import wraps

Role_Hierarchy = {
    "guest": 0,
    "user": 1,
    "moderator": 2,
    "admin": 3
}

def require_role(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")

            if not current_user:
                raise PermissionError("No user provided")

            user_role = current_user.get("role")

            if Role_Hierarchy[user_role] < Role_Hierarchy[required_role]:
                raise PermissionError(
                    f"Access denied. Required role: {required_role}, Your role: {user_role}"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_result(ttl=60):
    cache = {}
    lock = threading.Lock()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))  #documentations

            with lock:
                if key in cache:
                    result, t = cache[key]
                    if time.time() - t < ttl:
                        print("[CACHE] Hit")
                        return result

            print("[CACHE] Miss")
            result = func(*args, **kwargs)

            with lock:
                cache[key] = (result, time.time()) 

            return result

        return wrapper
    return decorator



class RateLimiter:

    def __init__(self, calls_per_minute: int = 10):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
        self.lock = threading.Lock()

    #documentations

