from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from datetime import date

import os

#init
app = Flask(__name__)

#to locate the database file; letting the server know where it is
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initlize the db
db = SQLAlchemy(app)

#initialize Marshmallow
ma = Marshmallow(app)


#Create a class for a Reservation (a name and a birthday)
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # birthday = db.Column(db.Date, nullable=False)

    # , birthday
    def __init__(self, name):
        self.name = name
        # self.birthday = birthday

#Creating a Reservation schema
class ReservationSchema(ma.Schema):
    class Meta:
        # , 'birthday'
        fields = ('id', 'name')

#Initialize the schema
reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------

#Route for adding a new reservation
@app.route('/reservation', methods=['POST'])
def add_reservation():
    name = request.json['name']
    # birthday = request.json['birthday']
    # , birthday
    new_reservation = Reservation(name)

    db.session.add(new_reservation)
    db.session.commit()

    return reservation_schema.jsonify(new_reservation)


#Route for getting all reservations
@app.route('/reservations', methods=['GET'])
def get_all_reservations():
    all_reservations = Reservation.query.all()
    result = reservations_schema.dump(all_reservations)
    return jsonify(result)


#Route for getting a single reservation
@app.route('/reservation/<id>', methods=['GET'])
def get_one_reservation(id):
    one_reservation = Reservation.query.get(id)
    return reservation_schema.jsonify(one_reservation)


#Route for updating reservation
@app.route('/reservation/<id>', methods=['PUT'])
def update_reservation(id):
    reservation = Reservation.query.get(id)

    name = request.json['name']
    # birthday = request.json['birthday']
    # , birthday
    
    reservation.name = name

    db.session.commit()

    return reservation_schema.jsonify(reservation)


#Route for deleting a single reservation
@app.route('/reservation/<id>', methods=['DELETE'])
def delete_one_reservation(id):
    deleted_reservation = Reservation.query.get(id)
    db.session.delete(deleted_reservation)
    db.session.commit()
    return reservation_schema.jsonify(deleted_reservation)

#To run the server
if __name__ == '__main__':
    app.run(debug=True)