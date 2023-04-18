from flask import Blueprint, request, jsonify
import mongo_commands
import sql_commands
import User
from logger import logger

sql = sql_commands.Db_Commands()

tasks = Blueprint('tasks', __name__)

@tasks.route('/gettasks', methods=['GET'])
def gettasks():
    user_id = request.args.get('user_id')
    user = sql.get_user_by_id(user_id)
    if user is None:
        logger.warning(f'no user with uid {user_id} found')
        return {"tasks": []}
    return mongo_commands.get_user_tasks(user_id)

@tasks.route('/addtask', methods=['POST'])
def addtask():
    data = request.get_json()
    user_id = data['user_id']
    description = data['data']['description']
    logger.info(f'data is: {data}')
    if not description or not user_id:
        return {'status_code': 403, 'message': 'description, or user_id is missing'}
    return mongo_commands.add_task(user_id, description)

@tasks.route('/deletetask', methods=['DELETE'])
def deletetask():
    try:
        task_id = request.args.get('tid')
        logger.info(f'deleting task {task_id}')
        return mongo_commands.delete_task(task_id)
    except Exception as e:
        logger.error(f'exception caught {e} when tried to delete a task')
        return {'status_code': 200, 'message': e}

@tasks.route('/updatetaskstatus', methods=['PUT'])
def updatetask():
    data = request.get_json()
    tid = data['params']['tid']
    return mongo_commands.update_task_status(tid)