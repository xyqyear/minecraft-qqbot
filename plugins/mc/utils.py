def no_session(func):
    """if there the session argument is not required, we can use this decorator"""
    def wrapper(session, *args, **kw):
        return func(*args, **kw)
    return wrapper
