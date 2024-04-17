def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "throttling_rate_limt", limit)
        if key:
            setattr(func, "throttling_key", key)
        return func
    return decorator