from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_session import Session
import sql_commands
from config import ApplicationConfig
from api.tasks import tasks
from api.token import token
from api.auth import auth


sql = sql_commands.Db_Commands()
app = Flask(__name__)
app.config.from_object(ApplicationConfig)
server_session = Session(app)
app.register_blueprint(tasks, url_prefix='/api')
app.register_blueprint(token, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/api')

CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response


@app.route('/users/<username>', methods=['GET', 'DELETE'])
def users(username):
    if request.method == 'GET':
        user = sql.get_user_by_email(username)
        print(user)
        if user is None:
            return "User not found"
        return jsonify({"user": user.__dict__})
    elif request.method == 'DELETE':
        ####TBD####
        pass


if __name__ == '__main__':
    from waitress import serve
    from paste.translogger import TransLogger
    serve(TransLogger(app, setup_console_handler=False))