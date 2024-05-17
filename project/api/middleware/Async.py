from functools import wraps
from flask import jsonify

def asyncMiddleware(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        try:
            return await handler(*args, **kwargs)
        except Exception as ex:
            return jsonify({"Unhandled Error": str(ex)}), 500
    return wrapper