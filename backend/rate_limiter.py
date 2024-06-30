from collections import defaultdict
import time
from fastapi import HTTPException, Depends
from functools import wraps
from .database import get_api_key

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_rate_limited(self, key: str, limit: int, period: int) -> bool:
        current_time = time.time()
        self.requests[key] = [req for req in self.requests[key] if req > current_time - period]
        if len(self.requests[key]) >= limit:
            return True
        self.requests[key].append(current_time)
        return False

rate_limiter = RateLimiter()

def rate_limit(limit: int = 10, period: int = 3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, api_key: str = Depends(get_api_key), **kwargs):
            if rate_limiter.is_rate_limited(api_key, limit, period):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            return await func(*args, api_key=api_key, **kwargs)
        return wrapper
    return decorator