# Required Imports
import os
import re
from flask import Flask, request, jsonify, url_for
from firebase_admin import credentials, firestore, initialize_app
from flask.templating import render_template# Initialize Flask App
import json
import base64
import uuid
from werkzeug.utils import redirect

# FIREBASE_SERVICE_KEY = json.loads(base64.b64decode(os.environ['FIREBASE_SERVICE_KEY']))

app = Flask(__name__)# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')


class Task:
    def __init__(self, title):
        self.id = str(uuid.uuid1())
        self.title = title
        self.status = False

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        task = Task(request.form['title'])
        record = json.dumps(task.__dict__)
        id = record.get('id')
        todo_ref.document(id).set(record)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        todo : Return document that matches query ID
        all_todos : Return all documents    """
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')    
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/update', methods=['GET', 'POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return redirect("/")
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        # return jsonify({"success": todo_id}), 200
        if todo_id:
            todo_ref.document(todo_id).delete()
            return redirect('/')
        else:
            return "Id not found"
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            task = Task(request.form['title'])
            # record = json.dumps(task.__dict__)
            id = task.id
            todo_ref.document(id).set(task.__dict__)
            return redirect('/')
        except:
            return "there was an issue while adding your task"
    elif request.method == 'GET':
        try:
            todos = []
            for doc in todo_ref.stream():
                todo = doc.to_dict()
                todo['id'] = doc.id
                todos.append(todo)
            print(todos)
            return render_template('index.html', todos=todos)
        except:
            return "there was an issue loading your todos"



port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)