import datetime
from typing import Any, Dict, Optional, Tuple

__cache: Dict[Tuple[str, ...], Any] = {}
lifetime_in_hours: float = 2.0


def get_weather(city: str):
    key = __create_key(city)
    data = __cache.get(key)
    if not data:
        return None

    last = data['time']
    date = datetime.datetime.now() - last
    if date / datetime.timedelta(minutes=60) < lifetime_in_hours:
        return data['value']

    del __cache[key]
    return None


def set_weather(city: str, value: Optional[Dict[str, Any]]) -> None:
    key = __create_key(city)
    __cache[key] = {'time': datetime.datetime.now(), 'value': value}
    __clean_out_of_date()


def __create_key(city: str):
    if not city:
        raise RuntimeError("City is required")
    return city.strip().lower()


def __clean_out_of_date() -> None:
    for key, data in list(__cache.items()):
        date = datetime.datetime.now() - data.get('time')
        if date / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]