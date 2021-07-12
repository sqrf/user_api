from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Address(db.Model):
    __tablename__ = "address"
    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', name="fk_address_user_id"))
    postal_code = db.Column(db.String(5))
    municipality = db.Column(db.String(32))
    state = db.Column(db.String(32))
    primary_address = db.Column(db.Boolean)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        sqla_session = db.session
        # include_fk = True
        load_instance = True
