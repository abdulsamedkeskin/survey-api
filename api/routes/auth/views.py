from flask import Blueprint, request, jsonify
from api import bcrypt, key
from api.routes.user.middleware import login_required
from api.routes.user.models import User
import jwt
from datetime import datetime, timedelta


auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/register", methods=['POST'])
def register():
    body = request.get_json()
    User(username=body['username'], password=bcrypt.generate_password_hash(body['password'])).save()
    return {"success": True, "message": "User registered"}, 200

@auth.route("/login", methods=['POST'])
def login():
   body = request.get_json()
   user = User.objects(username=body['username'])[0]   
   if bcrypt.check_password_hash(user['password'], body['password']) == False:
      return jsonify({"status": 401, "message": "wrong password"}), 401
   else:
      payload = user.payload()
      payload.update({"exp":datetime.utcnow() + timedelta(hours=2)})
      token = jwt.encode(payload, key)
      return jsonify({"status": 200, "data": {"accessToken": token}}), 200


@auth.route("/refresh", methods=['POST'])
@login_required
def refresh(payload):
   payload.update({"exp": datetime.utcnow() + timedelta(hours=2)})
   token = jwt.encode(payload, key)
   return {"status": 200,"data": {"accessToken": token}}, 200
