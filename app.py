from flask import Flask, jsonify, request
from datetime import datetime
import hashlib
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api=Api(app, version='1.0', title='Todo API', description='A simple Todo API')

todo_ns = api.namespace('todos', description='Todo operations')

todo_list = []

todo_model = api.model('Todo', {
    'id': fields.String(readOnly=True, description='unique identifier'),
    'description': fields.String(required=True, description='description of todo item'),
    'date_created': fields.String(readOnly=True, description='date item created'),
    'date_updated': fields.String(readOnly=True, description='date item updated'),
    'date_completed': fields.String(description='date item marked as completed'),
    'completed': fields.Boolean(description='completion status of todo item')
})

def generatehash(description):
    return hashlib.md5(description.encode("utf-8")).hexdigest()

def get_current_time():
    return str(datetime.now())[:-7]



@todo_ns.route('/')
class TodoListResource(Resource):
    @todo_ns.marshal_list_with(todo_model, envelope='todo_list')
    def get(self):
        return todo_list, 200


    @todo_ns.expect(todo_model)
    @todo_ns.response(201, 'To-Do item created')
    @todo_ns.response(400, 'Bad Request')
    def post(self):
        request_data=api.payload
        description = request_data.get('description')
        id = request_data.get('id', None)
        current_time = get_current_time()
        completed=request_data.get('completed', False)

        # mark as completed
        if completed:
            for todo in todo_list:
                if todo["id"] == id:
                    if todo["completed"]:
                        return {"message": "Item is already marked as completed"}, 400
                    todo["completed"] = True
                    todo["date_completed"] = current_time
                    return {"message": "Item marked as completed", "todo": todo}, 200
            return {"error": "Todo item not found"}, 404


        # update item
        if id:
            for todo in todo_list:
                if id == todo["id"]:
                    todo["id"] = generatehash(description)
                    todo["description"] = description
                    todo["date_updated"] = current_time
                    return {'message': f'Item {id} updated successfully', 'todo': todo}, 200
            return {"error": "Todo item not found"}, 404

        # create item
        else:
            todo_id = generatehash(description)
            for todo in todo_list:
                if todo["id"] == todo_id:
                    return {"error": "Item with the same description already exists"}, 400

            new_todo_item = {
                "id": todo_id,
                "description": description,
                "date_created": current_time,
                "date_updated": current_time,
                "date_completed": None,
                "completed": False,
            }
            todo_list.append(new_todo_item)
            return {'message': 'New item created in to-do list', 'todo': new_todo_item}, 201


if __name__ == "__main__":
    app.run(debug=True)