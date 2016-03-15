from flask import Flask,jsonify,abort,make_response,request,url_for
from flask.ext.httpauth import HTTPBasicAuth	

auth = HTTPBasicAuth()	

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


#adding security to the apis
#here we just checked it simply but in real life we will check it using database
@auth.get_password   #decorator
def get_password(username):
    if username == 'abhishek':
        return 'you_wanna_my_password'
    return none 

#error callback for handling the error 401 i.e unauthorized error
@app.errorhandler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized error'}),403)


#the problem with the current design of api is  that the clients are
#forced to construct uri from the task identifiers that are returned
#it indirectly forces clents that to knnow how these uri needs to be built

#so a helper function that generated a public version of the task send to the client
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id=task['id'],_external=True)
        else:
            new_task[field] = task[field]
    return new_task

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
@auth.login_required
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task':task[0]})


#api get get all  the tasks
@app.route('/todo/api/v1.0/tasks',methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks':[make_public_task(task) for task in tasks]})  #similar to the map function in the javascript

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
