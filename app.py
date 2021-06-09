from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# NoteKeeping database, contains a three columns id (primary key), plant_name and date watered
class NoteKeeping(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    plant_name = db.Column(db.String(200), nullable=False)
    date_watered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# adds new plant to database and sets given name, and watered date to today
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['plant_name']
        new_note = NoteKeeping(plant_name=note_content)

        if note_content != "":
            try:
                db.session.add(new_note)
                db.session.commit()
                return redirect('/')
            except:
                return "Error: Unable to add note"
        else:
            notes = NoteKeeping.query.order_by(NoteKeeping.date_watered).all()
            error_msg = "New plant must have a name!"
            return render_template('index.html', notes=notes, error_msg=error_msg)
    else:
        notes = NoteKeeping.query.order_by(NoteKeeping.date_watered).all()
        return render_template('index.html', notes=notes)

# deletes plant with given id from the database
@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = NoteKeeping.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return "Error: unable to delete." + str(e)

# updates the watered date to today of plant with given id with
@app.route('/update/<int:id>')
def update(id):
    note = NoteKeeping.query.get_or_404(id)
    note.date_watered = datetime.utcnow()
    print(note.date_watered)

    try:
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return "Error: unable to update." + str(e)


if __name__ == "__main__":
    try:
        db.create_all()
    except Exception as e:
        print('Could not create new database.' + str(e))
    app.run(debug=True)
