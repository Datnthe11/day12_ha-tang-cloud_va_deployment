import time
import redis
from fastapi import HTTPException
from app.config import settings

# Kết nối tới Redis
r = redis.from_url(settings.redis_url)

def check_and_record_cost(user_id: str, input_tokens: int, output_tokens: int):
    """
    Sử dụng Redis để tính toán và lưu trữ chi phí (Cost Guard).
    """
    month_key = time.strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    # Tính toán chi phí cho request này
    # Giả định: GPT-3.5-turbo ($0.0015 / 1k input, $0.002 / 1k output)
    cost = (input_tokens / 1000) * 0.0015 + (output_tokens / 1000) * 0.002
    
    current_cost = r.get(key)
    if current_cost is None:
        current_cost = 0.0
    else:
        current_cost = float(current_cost)
        
    if current_cost + cost > settings.daily_budget_usd:
        raise HTTPException(503, f"Budget exhausted. Current usage: ${current_cost:.2f} / ${settings.daily_budget_usd:.2f}")
        
    # Ghi nhận chi phí mới
    r.incrbyfloat(key, cost)
    # Đặt thời gian hết hạn là 32 ngày (hơn 1 tháng)
    r.expire(key, 32 * 24 * 3600)
    
def get_current_cost(user_id: str) -> float:
    month_key = time.strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    val = r.get(key)
    return float(val) if val else 0.0
