from flask import Flask, render_template

app = Flask(__name__)

DEVELOPMENT_ENV = True

app = Flask(__name__)


@app.route('/')
def index(app_data=None):
    return render_template('homepage.html', app_data=app_data)


@app.route('/dashboard')
def dashboard(app_data=None):
    return render_template('dashboard.html', app_data=app_data)

@app.route('/control')
def control(app_data=None):
    return render_template('control.html', app_data=app_data)

if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
