from cachetools import TTLCache

from .conf import settings

cache = TTLCache(1000, settings.RATE_LIMIT_TIME)
