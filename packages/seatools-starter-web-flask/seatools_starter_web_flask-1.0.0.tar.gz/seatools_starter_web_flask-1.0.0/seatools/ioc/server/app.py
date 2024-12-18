from seatools.ioc import Autowired
from flask import Flask


def wsgi_app():
    """server wsgi app factory."""
    # Get Flask instance from ioc_bean()
    return Autowired(cls=Flask).ioc_bean()


def asgi_app():
    """server asgi app factory."""
    from uvicorn.middleware.wsgi import WSGIMiddleware
    app = wsgi_app()
    return WSGIMiddleware(app)
