from . import bp as api
from app.models import User
from app.site_blueprint.admin.auth import basic_auth, token_auth
from flask import request, make_response, g, abort
# from helpers import require_admin


@api.get('/token')
@basic_auth.login_required()
def get_token():
    user = g.current_user
    token = user.get_token()
    return make_response({"token":token}, 200)


@api.post('/user')
def post_user():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        abort(422)
    new_user = User()
    new_user.register(data)
    new_user.save()
    return make_response("success",200)


@api.put('/admin/<int:id>')
@token_auth.login_required()
# @require_admin
def make_admin(id):
    # Check the user id exists
    u=User.query.get(id)
    if not u:
        abort(404)
    # Make admin
    u.is_admin=True
    u.save()
    return make_response(f'{u.name_first} {u.name_last} is now an Admin', 200)
    
### NEW
@api.get('/login')
@basic_auth.login_required()
def get_login():
    user = g.current_user
    token = user.get_token()
    return make_response({"token":token, **user.to_dict()}, 200)
