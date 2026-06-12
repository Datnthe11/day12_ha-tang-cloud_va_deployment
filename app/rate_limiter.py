import time
import redis
from fastapi import HTTPException
from app.config import settings

# Kết nối tới Redis
r = redis.from_url(settings.redis_url)

def check_rate_limit(user_id: str):
    """
    Giới hạn số request/phút sử dụng Redis (Sliding window log hoặc Token bucket đơn giản)
    Ở đây sử dụng List lpush và ltrim để làm sliding window đơn giản.
    """
    now = int(time.time())
    key = f"rate_limit:{user_id}"
    
    # Bắt đầu transaction
    pipe = r.pipeline()
    # Loại bỏ các request cũ hơn 60 giây
    pipe.zremrangebyscore(key, 0, now - 60)
    # Đếm số lượng request trong 60 giây qua
    pipe.zcard(key)
    # Thêm request hiện tại vào
    import uuid
    pipe.zadd(key, {f"{now}-{uuid.uuid4().hex[:8]}": now})
    # Đặt TTL cho key
    pipe.expire(key, 60)
    
    results = pipe.execute()
    request_count = results[1]
    
    if request_count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
