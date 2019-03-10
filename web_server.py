from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///levels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), unique=False, nullable=False)
    file = db.Column(db.String(300), unique=False, nullable=False)

    def __repr__(self):
        return '<Level {} {} {}>'.format(
            self.id, self.file_name, self.file)


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('load.html')
    elif request.method == 'POST':
        f = request.files['file']
        load_level = f.read()
        num = len(Level.query.all()) + 1
        new_level = Level(file_name=str(num) + '_levels.txt', file=load_level)
        db.session.add(new_level)
        db.session.commit()
        return render_template('new_load.html')


@app.route('/get_files', methods=['GET'])
def get_files(num_file):
    file = Level.query.all()
    f = dict()
    for i in file:
        f[i.file_name] = i.file
    return f


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
