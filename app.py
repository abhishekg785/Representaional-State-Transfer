from flask import Flask,jsonify,abort,make_response

app = Flask(__name__)

tasks = [
    {
        'id':1,
        'title':'Buy Groceries',
        'description':'milk,cheese,pizza,apple',
        'done':False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)

#api get the task corresponding to a particuar task
@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task':task[0]})

#api get get all  the tasks
@app.route('/todo/api/v1.0/tasks',methods = ['GET'])
def get_tasks():
    return jsonify({'tasks':tasks})

if(__name__ == '__main__'):
    app.run(debug=True)
