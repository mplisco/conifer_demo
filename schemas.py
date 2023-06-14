from marshmallow import Schema, fields, validate

class PlainUserSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=3))
    last_name = fields.String(required=True, validate=validate.Length(min=3))
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserSchema(PlainUserSchema):
    contacts = fields.Nested('PlainContactSchema', many=True, dump_only=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class UserUpdateSchema(Schema):
    first_name = fields.String(required=False, validate=validate.Length(min=3))
    last_name = fields.String(required=False, validate=validate.Length(min=3))
    username = fields.String(required=False, validate=validate.Length(min=3))
    email = fields.Email(required=False)
    password = fields.String(required=False, validate=validate.Length(min=6))

class PlainContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=3))
    last_name = fields.String(required=True, validate=validate.Length(min=3))
    contact_frequency = fields.String(required=True)
    email = fields.Email(required=False)
    phone_number = fields.String(required=False)
    birthday = fields.Date(required=False)
    user_id = fields.Integer(required=True, dump_only=False)

# class ContactSchema(PlainContactSchema):
#     user_id = fields.Integer(required=True, load_only=True)
#     # user = fields.Nested(UserSchema(), dump_only=True)

class ContactUpdateSchema(Schema):
    first_name = fields.String(required=False, validate=validate.Length(min=3))
    last_name = fields.String(required=False, validate=validate.Length(min=3))
    contact_frequency = fields.String(required=False)
    email = fields.Email(required=False)
    phone_number = fields.String(required=False)
    birthday = fields.Date(required=False)