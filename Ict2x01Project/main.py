from flask import Flask, render_template

app = Flask(__name__)

DEVELOPMENT_ENV  = True

app = Flask(__name__)


@app.route('/')
def index(app_data=None):
    return render_template('index.html', app_data=app_data)

@app.route('/DashBoard')
def DashBoard(app_data=None):
    return render_template('DashBoard.html', app_data=app_data)

if __name__ == '__main__':
    app.run()