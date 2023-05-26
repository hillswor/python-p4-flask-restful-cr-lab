#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        response_dict_list = [plant.to_dict() for plant in Plant.query.all()]

        if not response_dict_list:
            return make_response(jsonify({"error": "No plants found"}), 404)

        return make_response(jsonify(response_dict_list), 200)

    def post(self):
        plant = Plant(**request.json)
        db.session.add(plant)
        db.session.commit()

        return make_response(jsonify(plant.to_dict()), 201)


api.add_resource(Plants, "/plants")


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)

        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        return make_response(jsonify(plant.to_dict()), 200)


api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
