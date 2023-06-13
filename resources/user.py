from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import UserModel
from schemas import UserSchema, UserLoginSchema, UserUpdateSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.find_by_email(user_data["email"]):
            abort(400, message="A user with that email already exists.")

        user = UserModel(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        user.save_to_db()

        return {"message": "User created successfully."}, 201

@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.find_by_email(user_data["email"])

        if user and user.password == user_data["password"]:
            return {"message": "User logged in successfully."}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    def get(self):
        return {"message": "Successfully logged out"}, 200

@blp.route("/users/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        return user

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")
        user.delete_from_db()
        return {"message": "User deleted."}, 200

    @blp.arguments(UserUpdateSchema)
    def patch(self, user_data, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message="User not found.")

        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.username = user_data["username"]
        user.email = user_data["email"]
        user.password = user_data["password"]

        user.save_to_db()
        return {"message": "User updated successfully."}, 200
