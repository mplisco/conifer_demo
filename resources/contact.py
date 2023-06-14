from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ContactModel
from schemas import PlainContactSchema, ContactUpdateSchema

blp = Blueprint("Contacts", "contacts", description="Operations on contacts")

@blp.route("/contacts")
class ContactList(MethodView):
    @blp.response(200, PlainContactSchema(many=True))
    def get(self):
        return ContactModel.query.all()

    @blp.arguments(PlainContactSchema)
    @blp.response(201, PlainContactSchema)
    def post(self, contact_data):
        contact_data['contact_frequency'] = contact_data['contact_frequency'].lower()
        contact = ContactModel(**contact_data)

        try:
            db.session.add(contact)
            db.session.commit()
        except AssertionError:
            abort(400, message="Invalid contact frequency provided.")
        except SQLAlchemyError:
            abort(500, message="Could not save contact.")

        return contact, 201

@blp.route("/users/<int:user_id>/contacts")
class UserContact(MethodView):
    @blp.response(200, PlainContactSchema(many=True))
    def get(self, user_id):
        contacts = ContactModel.query.filter_by(user_id=user_id).all()
        return contacts

@blp.route("/contacts/<int:contact_id>")
class Contact(MethodView):
    @blp.response(200, PlainContactSchema)
    def get(self, contact_id):
        contact = ContactModel.query.get_or_404(contact_id)
        return contact

    def delete(self, contact_id):
        contact = ContactModel.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contact deleted successfully."}, 200

    @blp.arguments(ContactUpdateSchema)
    @blp.response(200, PlainContactSchema)
    def patch(self, contact_data, contact_id):
        contact = ContactModel.query.get_or_404(contact_id)

        if not contact:
            abort(404, message="Contact not found.")

        contact.first_name = contact_data.get("first_name", contact.first_name)
        contact.last_name = contact_data.get("last_name", contact.last_name)
        contact.contact_frequency = contact_data.get("contact_frequency", contact.contact_frequency).lower()
        contact.email = contact_data.get("email", contact.email)
        contact.phone_number = contact_data.get("phone_number", contact.phone_number)
        contact.birthday = contact_data.get("birthday", contact.birthday)

        try:
            contact.save_to_db()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Could not update contact.")

        return contact, 200