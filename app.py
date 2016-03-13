from flask import Flask,jsonify,abort,make_response,request

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

#api for deleting a particular task
@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})


#api for posting the data
@app.route('/todo/api/v1.0/tasks',methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
              'id':tasks[-1]['id']+1,
              'title':request.json['title'],
              'description':request.json.get('description',""),
              'done':False
           }
    print 'REQUEST.JSON',request.json
    tasks.append(task)
    return jsonify({'task':task}),201


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

#api for updating the data
@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    task[id]['title'] = request.json.get('title')
    task[id]['description'] = request.json.get('description')
    task[id]['done'] = request.json.get('done')
    return jsonify({'task':task[0]})

if(__name__ == '__main__'):
    app.run(debug=True)
