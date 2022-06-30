import json
from lib2to3.pgen2 import token
import re
from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route ('/getdata')
@token_required
def getdata(current_user_token):
    return{'some':'value'}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    top_speed = request.json['top_speed']
    max_horsepower = request.json['max_horsepower']
    seats = request.json['seats']
    price = request.json['price']
    length = request.json['length']
    country = request.json['country']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    car = Car(make, model, year, top_speed, max_horsepower, seats, price, length, country, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

# Retrieve all Car Endpoints
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve Single Car Endpoint
@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# Update a Car
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.top_speed = request.json['top_speed']
    car.max_horsepower = request.json['max_horsepower']
    car.seats = request.json['seats']
    car.price = request.json['price']
    car.length = request.json['length']
    car.country = request.json['country']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete a Car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)