from flask import Blueprint, request, jsonify, session
import bcrypt
import sql_commands
import mongo_commands

sql = sql_commands.Db_Commands()

auth = Blueprint('auth', __name__)

@auth.route('/@me')
def get_current_user():
    user_session = session.get('user')
    if not user_session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(user_session)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data["email"]
    if not email:
        return jsonify({"message": "Bad username or password"}), 401
    password = data["password"]
    result = sql.get_password(email)
    if not result:
        return jsonify({"message": "Bad username or password"}), 401
    hashed_password = result.decode().rstrip("\x00").encode()
    # Check if the password matches the one provided by the user
    if hashed_password is not None:
        # Fetch the hashed password from the result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            # password is correct, redirect to welcome page
            user = sql.get_user_by_email(email)
            session['user'] = user
            print(session.get('user'))
            return jsonify(user), 200
        else:
            # password is incorrect, return an error message
            return jsonify({"message": "Bad username or password"}), 401
    else:
        # user does not exist, return an error message
        return jsonify({"message": "Bad username or password"}), 401

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not all(data[key] for key in data):
        return jsonify({"message": "Please make sure all field are filled"}), 403
    email = data['email']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    # hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        result = sql.create_user(email,hashed_password,first_name,last_name)
        if result:
            return jsonify({"message": f"{email} was created successfully"}), 200
        return jsonify({"message": "This email already exists"}), 403
    except Exception as e:
        return jsonify({"message": e}), 403

@auth.route('/logout', methods=['POST'])
def logout():
    user = session.get('user')
    if user:
        session.pop('user')
        return jsonify({'message': f'user {user["id"]} was logged out'}), 200
    return jsonify({'message': 'must log in to log out'}), 404

# @auth.route('/getcookie')
# def getcookie():
#     try:
#         session = request.cookies.get('session')
#         return jsonify({'session': session}), 200
#     except Exception as e:
#         return jsonify({'session': 'no session was found, please log in'}), 404

