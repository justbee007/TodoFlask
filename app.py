from threading import Thread
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from redisqueue import execute_redis_fn
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.getcwd()+'/test.db'
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    secretkey = os.environ.get("SECRET_KEY")
    print(secretkey)
    if request.method=='POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            execute_redis_fn()
            print("Task sent to redis queue")
            return redirect('/')
        except Exception as error:
            return "There is an issue"


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        print(tasks)
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')    
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as error:
        return "There is an error" 
@app.route('/update/<int:id>')    
def update(id):
    
    try:
        task = Todo.query.get_or_404(id)
        if(request.method =='POST'):
            task.content = request.form['content']
        
            db.session.commit()
            return redirect("/")    
        else:
            return render_template("update.html",task = task)
        # db.session.delete(task_to_delete)
        # db.session.commit()
        # return redirect("/")
    except Exception as error:
        return "There is an error"            
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)
