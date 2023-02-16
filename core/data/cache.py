
from typing import Any, Callable
from functools import wraps
import hashlib
import pickle
import logging
from core.config import CoreConfig

cfg:CoreConfig = None # type: ignore
# Make memcache optional
try:
    import pylibmc  # type: ignore
    has_mc = True
except ModuleNotFoundError:
    has_mc = False

def cached(lifetime: int=10, extra_key: Any=None) -> Callable:
    def _cached(func: Callable) -> Callable:
        if has_mc:
            hostname = "127.0.0.1"
            if cfg:
                hostname = cfg.database.memcached_host
            memcache = pylibmc.Client([hostname], binary=True)
            memcache.behaviors = {"tcp_nodelay": True, "ketama": True}
            
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                if lifetime is not None:

                    # Hash function args
                    items = kwargs.items()
                    hashable_args = (args[1:], sorted(list(items)))
                    args_key = hashlib.md5(pickle.dumps(hashable_args)).hexdigest()

                    # Generate unique cache key
                    cache_key = f'{func.__module__}-{func.__name__}-{args_key}-{extra_key() if hasattr(extra_key, "__call__") else extra_key}'

                    # Return cached version if allowed and available
                    try:
                        result = memcache.get(cache_key)
                    except pylibmc.Error as e:
                        logging.getLogger("database").error(f"Memcache failed: {e}")
                        result = None
                        
                    if result is not None:
                        logging.getLogger("database").debug(f"Cache hit: {result}")
                        return result

                # Generate output
                result = func(*args, **kwargs)

                # Cache output if allowed
                if lifetime is not None and result is not None:
                    logging.getLogger("database").debug(f"Setting cache: {result}")
                    memcache.set(cache_key, result, lifetime)

                return result
        else:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

        return wrapper

    return _cached
