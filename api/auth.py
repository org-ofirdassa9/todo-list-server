from flask import Blueprint, request, jsonify, session
import bcrypt
import sql_commands
import mongo_commands
from logger import logger

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
        logger.info(f'sign in not worked for {email}')
        return jsonify({"message": "Bad username or password"}), 403
    password = data["password"]
    result = sql.get_password(email)
    if not result:
        logger.info(f'sign in not worked for {email}')
        return jsonify({"message": "Bad username or password"}), 403
    hashed_password = result.decode().rstrip("\x00").encode()
    # Check if the password matches the one provided by the user
    if hashed_password is not None:
        # Fetch the hashed password from the result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            # password is correct, redirect to welcome page
            user = sql.get_user_by_email(email)
            session['user'] = user
            logger.info(f'user {email} sign in successfully')
            return jsonify(user), 200
        else:
            # password is incorrect, return an error message
            logger.info(f'sign in not worked for {email}')
            return jsonify({"message": "Bad username or password"}), 403
    else:
        # user does not exist, return an error message
        logger.info(f'sign in not worked for {email}')
        return jsonify({"message": "Bad username or password"}), 403

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not all(data[key] for key in data):
        logger.info(f'not all fields were filled when tried to sign up')
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
            logger.info(f'{email} was created successfully')
            return jsonify({"message": f"{email} was created successfully"}), 200
        logger.info(f'{email} already exists in the system')
        return jsonify({"message": "This email already exists"}), 403
    except Exception as e:
        logger.error(f'exception caught {e} when tried to sign up')
        return jsonify({"message": e}), 403

@auth.route('/logout', methods=['POST'])
def logout():
    user = session.get('user')
    if user:
        session.pop('user')
        logger.info(f'{user} was signed out')
        return jsonify({'message': f'user {user["id"]} was logged out'}), 200
    logger.warning(f'{user} tried to sign out without signing in')
    return jsonify({'message': 'must log in to log out'}), 404

# @auth.route('/getcookie')
# def getcookie():
#     try:
#         session = request.cookies.get('session')
#         return jsonify({'session': session}), 200
#     except Exception as e:
#         return jsonify({'session': 'no session was found, please log in'}), 404

