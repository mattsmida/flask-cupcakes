"""Flask app for Cupcakes"""

import os
from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcakes')
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get("/api/cupcakes")
def list_all_cupcakes():
    """ Returning JSON of all cupcakes

    Example response:
    {
	"cupcakes": [
		{
			"flavor": "chocolate",
			"id": 2,
			"image_url": "https://www.bakedbyrachel.com/...jpg
			"rating": 9,
			"size": "small"
		},
        ...
        ]}
    """

    cupcakes = Cupcake.query.order_by(desc('rating')).all()
    serialized_cupcakes = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get_single_cupcake_data(cupcake_id):
    """ Return JSON with cupcake information about a single cupcake

    Example response:
    {
	"cupcake": {
		"flavor": "cherry",
		"id": 1,
		"image_url": "https://tinyurl.com/demo-cupcake",
		"rating": 5,
		"size": "large"
        }
    }
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = cupcake.serialize()

    return jsonify(cupcake=serialized_cupcake)


@app.post("/api/cupcakes")
def create_cupcake():
    """ Create a cupcake with flavor, size, rating, and image URL.

    JSON POST example:
        {
			"flavor": "chocolate",
			"rating": 8,
			"size": "medium",
			"image_url": "https://example.com/chocolate-cupcake.jpg"
        }

    Response:
	{"cupcake": {
		"flavor": "chocolate",
		"id": 13,
		"image_url": "https://example.com/chocolate-cupcake.jpg",
		"rating": 8,
		"size": "medium"
        }
    }
           """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json.get('image_url')

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image_url=image_url)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_cupcake = new_cupcake.serialize()

    return (jsonify(cupcake=serialized_cupcake), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def patch_cupcake(cupcake_id):
    """ Update a cupcake using the id passed in the URL
    Request body body may include flavor, size, rating and image data
    but not all fields are required

    JSON request example:
    {
			"flavor": "vanilla",
			"size": "big"
    }

    JSON response example (observe the change to flavor and size):
    {
        "cupcake": {
            "flavor": "vanilla",
            "id": 1,
            "image_url": "https://tinyurl.com/demo-cupcake",
            "rating": 5,
            "size": "big"
            }
    }

    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake_edits = request.json

    for key in cupcake_edits:            # TODO: Why didn't c[key] work?
        setattr(cupcake, key, cupcake_edits[key])  # Is setattr() right?

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = cupcake.serialize()

    return (jsonify(cupcake=serialized_cupcake), 200)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """ Delete a cupcake using the id passed in the URL.
    No request body needed.

    JSON response example of a successful deletion of cupcake id 27562:
    {
        "deleted": 27562
    }

    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)
