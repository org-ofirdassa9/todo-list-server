import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from logger import logger

client = MongoClient(f'mongodb://{os.environ["MONGO_USER"]}:{os.environ["MONGO_PASS"]}@{os.environ["MONGO_ADDR"]}/{os.environ["MONGO_DB_NAME"]}?authSource=admin&tls=false')
db = client['todolist']
tasks_collection = db['tasks']

# def add_user(user_id):
#     try:
#         existing_user = tasks_collection.find_one({'user.uid': user_id})
#         logger.info(existing_user)
#         if existing_user:
#             return {'status_code': 400, 'message': 'User already exists'}
#         user = {"user": {"uid": user_id, "tasks": []}}
#         tasks_collection.insert_one(user)
#         return {'status_code': 200, 'message': f'{user} has been added!'}
#     except Exception as e:
#         logger.info(e)

def add_task(user_id, description):
    try:
        logger.info((f'MONGO CONN STRING = mongodb://{os.environ["MONGO_USER"]}:{os.environ["MONGO_PASS"]}@{os.environ["MONGO_ADDR"]}/{os.environ["MONGO_DB_NAME"]}?authSource=admin&tls=false'))
        task = {'uid': user_id, 'task': {'description': description, 'completed': False}}
        logger.info(f'{user_id} {description} {task}')
        result = tasks_collection.insert_one(task)
        tid = str(task['_id'])
        logger.info(f'task added successfully task_id: {tid}')
        task['_id'] = tid
        return task
    except Exception as e:
        return {'status_code': 200, 'error_message': e}

def get_user_tasks(user_id):
    try:
        logger.info(f'getting tasks for user {user_id}')
        user_tasks_len = tasks_collection.count_documents({ "uid": int(user_id) })
        if user_tasks_len == 0:
            logger.warning(f'did not found any tasks for user {user_id}')
            return {"tasks": []}
        user_tasks = tasks_collection.find({ "uid": int(user_id) })
        tasks_list = []
        tasks_dict = {}
        for document in user_tasks:
            logger.info(f'document in user_tasks - {document}')
            task = {}
            task['description'] = document['task']['description']
            task['completed'] = document['task']['completed']
            task['tid'] = str(document['_id'])
            tasks_list.append(task)
        tasks_dict['tasks'] = tasks_list
        logger.info(f'found tasks - {tasks_dict}')
        return tasks_dict
    except Exception as e:
        logger.error(f'exception caught when tried fetching a users tasks\n {e}')

def delete_task(tid):
    try:  
        tasks_collection.delete_one({'_id': ObjectId(tid)})
        logger.info(f'deleted {tid} sucessfully')
        return {'tid': tid} 
    except Exception as e:
        logger.error(f'exception caught when tried fetching a users tasks\n {e}')
        return {'404': 'Not Found'}


def update_task_status(tid):
    try:
        completed = tasks_collection.find_one({"_id":  ObjectId(tid)})['task']['completed']
        if completed:
            tasks_collection.update_one({"_id": ObjectId(tid)}, {"$set": {"task.completed": False}})
            return {'tid': tid}
        tasks_collection.update_one({"_id": ObjectId(tid)}, {"$set": {"task.completed": True}})
        return {'tid': tid}
    except Exception as e:
        logger.info(e)
        return {'404': 'Not Found'}