from db import db
from sqlalchemy.orm import validates
from .base import BaseModel


class ContactModel(BaseModel):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    user = db.relationship('UserModel', back_populates='contacts')

    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    contact_frequency = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(), nullable=True)
    phone_number = db.Column(db.String(), nullable=True)
    birthday = db.Column(db.Date(), nullable=True)

    @validates('contact_frequency')
    def validate_contact_frequency(self, key, contact_frequency):
        valid_frequencies = ["weekly", "biweekly", "monthly", "quarterly"]
        if contact_frequency.lower() not in valid_frequencies:
            raise AssertionError('Invalid contact frequency provided')
        return contact_frequency


    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()