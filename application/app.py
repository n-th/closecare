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
    is_active = db.Column(db.Boolean)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.String(50), db.ForeignKey(Employee.id), unique=True
    )  # quem fica com os documentos quando a pessoa sai da empresa?
    document_type = db.Column(db.String(100))
    file = db.Column(db.String(70), unique=True)
    # expire = db.Column() after a time employee leaves


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
    # check if manager_id==null or if manager_id exists in employee(id) (ordem na insercao de dados?)

    added_employee = {}

    return make_response({"employee": added_employee}, 202)


@app.route("/employee/:id", methods=["PUT"])
def update_employee():
    # check if employee exists
    # check if new manager_id==null or if manager_id exists in employee(id)
    #

    # atomic
    # update employee
    # update position

    updated_employee = {}

    return make_response({"employee": updated_employee}, 202)


@app.route("/employee/:id", methods=["DELETE"])
def delete_employee():
    # check if employee exists
    # check if new manager_id==null or if manager_id exists in employee(id)
    #

    # atomic
    # update employee
    # update position

    updated_employee = {}

    return make_response({"employee": updated_employee}, 202)


@app.route("/employee/:id/documents", methods=["GET"])
def get_documents_per_employee():
    # check if manager_id==null or if manager_id exists in employee(id) (ordem na insercao de dados?)

    added_employee = {}
    documents = []

    return make_response({"employee": added_employee, "documents": documents}, 202)


if __name__ == "__main__":
    # app.register_blueprint(health_check)
    # app.register_blueprint(documents)
    # app.register_blueprint(employees)

    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
