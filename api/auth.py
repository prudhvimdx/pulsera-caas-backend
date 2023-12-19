from flask import request, jsonify, g
import hashlib
import hmac
import jwt
import datetime
import config 
from models import auth_models


def hash_password(password):
    # Ensure the key and password are bytes
    key = str(config.SECRET_KEY)
    if not isinstance(key, bytes):
        key = key.encode('utf-8')
    if not isinstance(password, bytes):
        password = password.encode('utf-8')
    # Create a new HMAC object using a key and the SHA-256 hash algorithm
    return hmac.new(key, password, hashlib.sha256).hexdigest()


def check_auth_token():
    # Exclude authentication check for specific routes (e.g., login)
    if request.path in ['/signin', '/checkEmail', '/signup']:
        return

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    print(token)
    try:
        data = jwt.decode(token, str(config.JWT_SECRET_KEY), algorithms=["HS256"])
        user_details = auth_models.User.objects(id=data["id"]).first()
        g.logged_in_user_details = user_details
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401


def generate_token(type, id):
    if type == "auth":
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=int(config.AUTH_TOKEN_EXPIRY_MINIUTES))
    if type == "refresh":
        exp = datetime.datetime.utcnow() + datetime.timedelta(days=int(config.REFRESH_TOKEN_EXPIRY_DAYS))
    return jwt.encode({'type':type, 'id': id, 'exp': exp}, str(config.JWT_SECRET_KEY), algorithm='HS256')


def check_email():
    req_data = request.get_json()
    email_users = auth_models.User.objects(email=req_data["email"])
    if len(email_users):
        return jsonify({"message": "User already available"}), 400
    return jsonify({"message": "User not available please proceed with Signup."}), 200



def signup():
    try:
        # Logic to register a user in MongoDB
        # users_db_manager = MongoDBManager(db, 'users')
        req_data = request.get_json()
        print(req_data)
        if not req_data or "email" not in req_data or "password" not in req_data:
            return jsonify({'message': 'Please provide Credentials!'}), 401
        # email_users = users_db_manager.find({"email": req_data["email"]})
        email_users = auth_models.User.objects(email=req_data["email"])
        if len(email_users):
            return jsonify({"message": "User already available"}), 400
        req_data["password"] = hash_password(req_data["password"])
        # user_id = users_db_manager.insert(req_data)
        new_user = auth_models.User(email=req_data["email"], password=req_data["password"])
        if 'first_name' in req_data:
            new_user.first_name = req_data['first_name']
        if 'last_name' in req_data:
            new_user.last_name = req_data['last_name']
        new_user.save()
        # TODO Need to implement Other logics like Send welcome Email, Send Verification email Etc.
        return jsonify({"message": f"Inserted user with ID: {str(new_user.id)}"}), 200
    except Exception as e:
        print("Error 2", e)
        return jsonify({"message": "Error While creating the USER!"}), 400


def signin():
    req_data = request.get_json()
    if not req_data or 'email' not in req_data or 'password' not in req_data:
        return jsonify({'message': 'Please provide Credentials!'}), 400
    user_details = auth_models.User.objects(email=req_data["email"]).first
    if user_details.login_blocked or user_details.unsuccessful_login_attempts >= 3:
        return jsonify({'message':'Your account was blocked due to multiple unsuccessful attempts'}), 400
    user = auth_models.User.objects(mail=req_data["email"], password=hash_password(req_data["password"]))
    if len(user):
        token = generate_token('auth', str(user[0].id))
        refresh_token = generate_token('refresh', str(user[0].id))
        return jsonify({'message': 'Login successful!', 'token': token, 'refresh_token': refresh_token}), 200
    else:
        user_details.unsuccessful_login_attempts = user_details.unsuccessful_login_attempts + 1
        if user_details.unsuccessful_login_attempts == 2:
            user_details.save()
            return jsonify({'message': 'Authentication failed!\nYou have one more attempt left to login if you need any help please contact helpdesk.'}), 401
        if user_details[0].unsuccessful_login_attempts >= 3:
            user_details.login_blocked = True
            user_details.save()
            return jsonify({'message': 'Authentication failed!\nYou have exxceed the login unsuccessful attempts, please contact helpdesk.'}), 401
        user_details.save()
        return jsonify({'message': 'Authentication failed!'}), 401


def login_history():
    return 
