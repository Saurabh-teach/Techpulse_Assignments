import time
import threading
from functools import wraps

def require_role(required_role: str):

    role_hierarchy = {
        "guest": 0,
        "user": 1,
        "moderator": 2,
        "admin": 3
    }

    if required_role not in role_hierarchy:
        raise ValueError("Invalid role")

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            current_user = kwargs.get("current_user")

            if not current_user:
                raise PermissionError("No user provided")

            user_role = current_user.get("role")

            if user_role not in role_hierarchy:
                raise PermissionError("Invalid user role")

            
            if role_hierarchy[user_role] < role_hierarchy[required_role]:
                raise PermissionError(
                    f"Access denied. Required: {required_role}, Your role: {user_role}"
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

            key = (args, tuple(sorted(kwargs.items())))

            with lock:
                if key in cache:
                    result, saved_time = cache[key]

                   
                    if time.time() - saved_time < ttl:
                        print("Cache Hit")
                        return result

            
            print("Cache Miss")
            result = func(*args, **kwargs)

            with lock:
                cache[key] = (result, time.time())

            return result

        return wrapper

    return decorator



class RateLimitExceeded(Exception):
    pass


class RateLimiter:

    def __init__(self, calls_per_minute=5):
        self.calls_per_minute = calls_per_minute
        self.call_times = []
        self.lock = threading.Lock()

    def __call__(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            current_time = time.time()

            with self.lock:

               
                self.call_times = [
                    t for t in self.call_times
                    if current_time - t < 60
                ]

                if len(self.call_times) >= self.calls_per_minute:
                    raise RateLimitExceeded("Too many calls. Try again later.")

                self.call_times.append(current_time)

            return func(*args, **kwargs)

        return wrapper


@require_role("admin")
def delete_user(user_id, current_user=None):
    return "Deleted"


@cache_result(ttl=30)
def get_data(query):
    time.sleep(0.1)
    return "result"


@RateLimiter(5)
def api_call():
    return "OK"


# Test

try:
    delete_user(1, current_user={"role": "guest"})
except PermissionError as e:
    print(e)

print(delete_user(1, current_user={"role": "admin"}))


get_data("test")   
get_data("test")   
get_data("new")    


for i in range(6):
    try:
        print(api_call())
    except RateLimitExceeded as e:
        print(e)