from functools import wraps
from flask import request, jsonify
from .utils import decodeToken

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"status": 401,"message": "token is not provided"}), 401
        token = token.split("Bearer ")[1]
        try:
            payload = decodeToken(token)
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({"status": 401, "message": str(e)}), 401
    return decorator