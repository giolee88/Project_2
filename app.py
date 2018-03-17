# import necessary libraries
import json
from flask import (
    Flask,
    render_template,
    jsonify,
    request)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome!"

if __name__ == "__main__":
    app.run(debug=True)
