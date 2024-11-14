from flask import Flask 

app = Flask(__name__)

@app.route('/')
# @app.route('/<name>')
def index():
    return '<h1>Hello World !!</h1>'
    # return '<h1>Hello {}!</h1>'.format(name)


