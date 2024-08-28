# Imports
from flask import Flask, request, render_template,url_for,redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_migrate import Migrate
from wtforms.widgets import TextArea

# My C.R.U.D app
app = Flask(__name__)

# Database configuration
# creating DB instance
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1969@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
app.config['SECRET_KEY'] = 'dsjvcnw4%*&TBVhv@$#3'

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# Creating ( C ) Models ~ Row of data
class Mytodo(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    degree = db.Column(db.String(500), nullable=False)
    #date_added = db.Column(db.DateTime, default=datetime)

    def __repr__(self):
        return self.id

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Add a todo
    if request.method == 'POST':
        content = request.form['content']#, widget:=TextArea()
        degree = request.form['degree']
        new_todo = Mytodo(content=content, degree= degree)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    
    # See all todos
    else:
        all_todo = Mytodo.query.order_by(Mytodo.id)
        return render_template('index.html', all_todo = all_todo)

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    delete_todo = Mytodo.query.get_or_404(id)
    try:
        db.session.delete(delete_todo)
        db.session.commit()
        flash('To-do Item Was Deleted Successfully!')
        return redirect(url_for('index'))
    except Exception as e:
            flash('Delete Was Not Successful !')
            return f"ERROR:{e}"


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    todo = Mytodo.query.get_or_404(id)
    if request.method == 'POST':
        todo.content = request.form['content']
        todo.degree = request.form['degree']
        try:
            db.session.commit()
            flash('To-do Item Was Updated Successfully !')
            return redirect('/')
        except:
            flash('To-do Update was Mot Successful !')
            return render_template('update.html')
    else:
        return render_template('update.html', todo=todo)


if __name__ == '__main__':
    
    app.run(debug=False)


'''
delete:
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    delete_todo = Mytodo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            db.session.delete(delete_todo)
            db.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"ERROR: {e}")
            return redirect(url_for('index'))
html side

<form >
    {% for todo in all_todo %}
                    
        <p >
            {{todo.content}}
            <br>
            <i>({{ todo.degree }})</i>
            <br>
            <div >
                <form   method="POST" action="/delete">
                    <!--Deleting a todo(button)-->
                    <button class="btn btn-danger">
                        <a href="{{ url_for('delete', id=todo.id)}}" style="color:White;">
                            Delete
                        </a>
                    </button> 

                    <!--Update a todo(button)/link to update page -->
                        <buttton class="btn btn-warning" >
                            <a href="{{ url_for('update', id=todo.id)}}" style="color:White;">
                                Update
                            </a>
                        </button>
                </form>
            </div>
        </p> 
        <br><br>
    {% endfor %}
</form>

Update
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

        todo = Mytodo.query.get_or_404(id)
        if request.method == 'POST':
            todo.content = request.form['content']
            todo.degree = request.form['degree']
            try:
                db.session.commit()
                flash("To-do Updated Successfully !")
                return redirect(url_for('index'))
            except Exception as e:
                print(f"ERROR: {e}")
                flash("ERROR!! To-do Was Not Updated !")
                return redirect(url_for('update'))
        else:
            return render_template('update.html')

update.html

<form method="POST" action="/update" >
                <br>
                <div>
                    <label for="content">
                        <h3>Add To-Do's</h3>
                    </label>
                    <br>
                    <input type="text" name="content" placeholder="Add your to-do's" class="form-control">
                </div>
                <br>
                <h3>
                    <label for="degree">
                        Importance
                    </label>
                </h3>
                <p>
                    <input
                    id="degree-0"
                    name="degree"
                    required
                    type="radio"
                    value="Important"
                    >
                    <label for="degree-0">Important</label>
                </p>
                <p>
                    <input
                    id="degree-1"
                    name="degree"
                    required
                    type="radio"
                    value="Unimportant"
                    >
                    <label for="degree-1">Unimportant</label>
                </p>
                <p>
                    <input
                    id="degree-2"
                    name="degree"
                    required
                    type="radio"
                    value="Very Important"
                    >
                    <label for="degree-2">Very Important</label>
                </p>
                <button type="submit" class="btn btn-success" >Submit</button>
            </form>
'''