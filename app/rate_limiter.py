from .redis_database import r_client
from datetime import datetime, timedelta,timezone
from uuid import UUID
from .utils import convert_utc_to_ist

MESSAGES_PER_DAY_LIMIT_FREE=7
MESSAGES_PER_DAY_LIMIT_PRO=10

def _user_key(user_id:UUID)->str:
    
    current_utc_datetime=datetime.now(timezone.utc)
    current_ist_datetime=convert_utc_to_ist(current_utc_datetime)
    current_ist_date=datetime.strftime(current_ist_datetime,"%Y-%m-%d")
    
    return f"User:{user_id}:Count:{current_ist_date}"

def _seconds_until_midnight():
    datetime_now_utc = datetime.now(timezone.utc)
    datetime_now_ist = convert_utc_to_ist(datetime_now_utc)

    date_tomorrow = datetime_now_ist.date() + timedelta(days=1)
    ist_offset = timedelta(hours=5, minutes=30)
    ist_timezone = timezone(ist_offset)

    datetime_tomorrow = datetime.combine(date_tomorrow, datetime.min.time(), tzinfo=ist_timezone)

    datetime_delta = datetime_tomorrow - datetime_now_ist

    return int(datetime_delta.total_seconds())

async def increment_message_counter(user_id: UUID, user_is_pro: bool) -> bool:
    key = _user_key(user_id)
    count = await r_client.get(key)
    seconds_until_midnight_reset=_seconds_until_midnight()
    
    limit = MESSAGES_PER_DAY_LIMIT_PRO if user_is_pro else MESSAGES_PER_DAY_LIMIT_FREE

    if count is None:
        await r_client.set(key, 1, ex=seconds_until_midnight_reset)
        return True

    if int(count) >= limit:
        return False

    async with r_client.pipeline() as pipe:
        await pipe.incr(key)
        await pipe.expire(key, seconds_until_midnight_reset)
        await pipe.execute()

    return True
        