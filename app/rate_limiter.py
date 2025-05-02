from .redis_database import r_client
from datetime import datetime,timezone
from uuid import UUID
from .utils import convert_utc_to_ist

MESSAGES_PER_DAY_LIMIT=5

def _user_key(user_id:UUID)->str:
    
    current_utc_datetime=datetime.now(timezone.utc)
    current_ist_datetime=convert_utc_to_ist(current_utc_datetime)
    current_ist_date=datetime.strftime(current_ist_datetime,"%Y-%m-%d")
    
    return f"User:{user_id}:Count:{current_ist_date}"

async def increment_message_counter(user_id: UUID) -> bool:
    key = _user_key(user_id)
    count = await r_client.get(key)

    if count is None:
        await r_client.set(key, 1, ex=86400)
        return True

    if int(count) >= MESSAGES_PER_DAY_LIMIT:
        return False

    async with r_client.pipeline() as pipe:
        await pipe.incr(key)
        await pipe.expire(key, 86400)
        await pipe.execute()

    return True
        