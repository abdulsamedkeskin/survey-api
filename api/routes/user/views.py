from flask import Blueprint, jsonify
from .models import User
from .middleware import login_required

user = Blueprint('users', __name__, url_prefix='/users')

@user.route("/me", methods=['GET'])
@login_required
def me(payload):
    user = User.objects(id=payload['identity'])[0]
    return jsonify(user)