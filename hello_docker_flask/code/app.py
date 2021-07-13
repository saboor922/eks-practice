from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return 'This is my Flask App in Kubernetes'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
