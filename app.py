"""Flask app for Cupcakes"""

import os
from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/api/cupcakes")
def list_all_cupcakes():
    """ Returning JSON of all cupcakes """

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)

@app.get("/api/cupcakes/<int:cupcake_id>")
def get_single_cupcake_data(cupcake_id):
    """ Return JSON with cupcake information """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = cupcake.serialize()

    return jsonify(cupcake=serialized_cupcake)

@app.post("/api/cupcakes")
def create_cupcake():
    """ Create a cupcake with flavor, size, rating, and image data """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json['image_url'] if request.json['image_url'] else None

    # TODO bugfix line 40 about image_url 
    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_cupcake = new_cupcake.serialize()

    return (jsonify(cupcake=serialized_cupcake), 201)

