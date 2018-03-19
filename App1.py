from flask import Flask, jsonify

coordinates_dictionary = {
   {"coordinates": "52 : 45", "City": "Seoul"},
   {"coordinates": "43 : 56", "City": "New York City"},
   {"coordinates": "45 : 32", "City": "Washington D.C."},
   {"coordinates": "56 : 67", "City": "London"},
   {"coordinates": "45 : 23", "City": "Tallahassee"},
   {"coordinates": "34 : 34", "CIty": "Oklahoma City"},
}

app = Flask(__name__)

@app.route("/<city>")
def cities_coordinates(city):

    canonicalized = city.replace(" ", "").lower()
    for coordinates in coordinates_dictionary:
        potential_match = coordinates.replace(" ", "").lower()

        if canonicalized == potential_match:
            return jsonify({'coordinates' : coordinates,
                            'city' : coordinates_dictionary[coordinates]})

    return jsonify ({"error": "City not found"}), 404

@app.route('/')
def graphs():
    #insert graphs here???



if __name__ == "__main__":
    app.run(debug=True)


