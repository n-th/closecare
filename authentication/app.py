import jwt
import uuid

from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://username:password@localhost:5432/dbname"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    company_id = db.Column(db.String(80))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "authorization" in request.headers:
            token = request.headers["authorization"]  # authorization: Bearer token

        if not token:
            return jsonify(message={"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(public_id=data["public_id"]).first()

        except Exception:
            return jsonify(message={"message": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/user", methods=["GET"])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    all_users = [{"public_id": user.public_id, "name": user.name, "email": user.email} for user in users]

    return jsonify(message={"users": all_users})


@app.route("/login", methods=["POST"])
def login():
    auth = request.form

    if not auth or not auth.get("email") or not auth.get("password"):
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm ="Login required"'})

    user = User.query.filter_by(email=auth.get("email")).first()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm ="User does not exist"'})

    if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                "public_id": user.public_id,
                "expires_at": datetime.now(timezone.utc) + timedelta(minutes=30),
                "issed_at": datetime.now(timezone.utc),
            },
            app.config["SECRET_KEY"],
        )

        return make_response(jsonify(message={"token": token.decode("UTF-8")}), 201)

    return make_response("Could not verify", 403, {"WWW-Authenticate": 'Basic realm ="Wrong Password"'})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.form

    name, email = data.get("name"), data.get("email")
    password = data.get("password")

    if user := User.query.filter_by(email=email).first():
        return make_response("User already exists. Please Log in.", 202)

    user = User(public_id=str(uuid.uuid4()), name=name, email=email, password=generate_password_hash(password))

    db.session.add(user)
    db.session.commit()

    return make_response("Successfully registered.", 201)


if __name__ == "__main__":
    app.run(debug=True)
