from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=3))
    last_name = fields.String(required=True, validate=validate.Length(min=3))
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserUpdateSchema(Schema):
    first_name = fields.String(required=False, validate=validate.Length(min=3))
    last_name = fields.String(required=False, validate=validate.Length(min=3))
    username = fields.String(required=False, validate=validate.Length(min=3))
    email = fields.Email(required=False)
    password = fields.String(required=False, validate=validate.Length(min=6))

