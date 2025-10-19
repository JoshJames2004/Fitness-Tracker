from flask import Flask, render_template, request, redirect, url_for
from database import db, Workout, Exercise
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return render_template('index.html', workouts=workouts)

@app.route('/workout/<date>', methods=['GET', 'POST'])
def workout(date):
    if request.method == 'POST':
        steps = int(request.form['steps'])
        # create or update workout
        workout = Workout.query.filter_by(date=date).first()
        if not workout:
            workout = Workout(date=date, steps=steps)
            db.session.add(workout)
        else:
            workout.steps = steps
        db.session.commit()
        return redirect(url_for('index'))
    workout = Workout.query.filter_by(date=date).first()
    return render_template('workout.html', workout=workout, date=date)

if __name__ == '__main__':
    app.run()




