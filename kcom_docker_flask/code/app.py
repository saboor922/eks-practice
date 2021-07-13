from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return """
      <h1>Hello KCOM!</h1>

      <img src="https://maps.googleapis.com/maps/api/staticmap?center=52.0494822,1.1581791&zoom=14&size=400x400&key=AIzaSyACiXeDnNqVVbk_yIknPSPt5u0e80R7xKg" alt="map of kcom">
  
    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8082)
