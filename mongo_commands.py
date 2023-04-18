import os
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(os.environ['MONGO_TODO_CONN'])
db = client['todolist']
tasks_collection = db['tasks']

# def add_user(user_id):
#     try:
#         existing_user = tasks_collection.find_one({'user.uid': user_id})
#         print(existing_user)
#         if existing_user:
#             return {'status_code': 400, 'message': 'User already exists'}
#         user = {"user": {"uid": user_id, "tasks": []}}
#         tasks_collection.insert_one(user)
#         return {'status_code': 200, 'message': f'{user} has been added!'}
#     except Exception as e:
#         print(e)

def add_task(user_id, description):
    try:
        task = {'uid': user_id, 'task': {'description': description, 'completed': False}}
        print(user_id, description, task)
        result = tasks_collection.insert_one(task)
        print(result)
        tid = str(task['_id'])
        task['_id'] = tid
        return task
    except Exception as e:
        return {'status_code': 200, 'error_message': e}

def get_user_tasks(user_id):
    try:
        user_tasks = tasks_collection.find({ "uid": user_id })
        tasks_list = []
        tasks_dict = {}
        for document in user_tasks:
            task = {}
            task['description'] = document['task']['description']
            task['completed'] = document['task']['completed']
            task['tid'] = str(document['_id'])
            tasks_list.append(task)
        tasks_dict['tasks'] = tasks_list
        return tasks_dict
    except Exception as e:
        print('ERROR')
        print(e)

def delete_task(tid):
    try:  
        tasks_collection.delete_one({'_id': ObjectId(tid)})
        return {'tid': tid} 
    except Exception as e:
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
        print(e)
        return {'404': 'Not Found'}