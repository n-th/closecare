import os

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://username:password@localhost:5432/dbname"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    manager_id = db.Column(db.String(50), unique=True)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True)
    document_type = db.Column(db.String(100))
    file = db.Column(db.String(70), unique=True)


@app.route("/healthcheck")
def health_check():
    return make_response({"message": "So far, so good."}, 202)


@app.route("/employee/", methods=["POST"])
def add_employee():
    # check if manager_id==null or if manager_id exists in employee(id)

    added_employee = {}

    return make_response({"employee": added_employee}, 202)


@app.route("/employees/", methods=["GET"])
def get_employees():
    # check if manager_id==null or if manager_id exists in employee(id)

    added_employee = {}

    return make_response({"employee": added_employee}, 202)


@app.route("/employee/:id", methods=["PUT"])
def update_employee():
    # check if employee exists
    # check if new manager_id==null or if manager_id exists in employee(id)
    #

    updated_employee = {}

    return make_response({"employee": updated_employee}, 202)


if __name__ == "__main__":
    # app.register_blueprint(health_check)
    # app.register_blueprint(documents)
    # app.register_blueprint(employees)

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
