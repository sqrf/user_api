from datetime import datetime
from config import db
from models.address import Address, AddressSchema
# https://stackoverflow.com/questions/61810855/sqlalchemy-orm-exc-unmappedinstanceerror-class-builtins-dict-is-not-mapped
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, fields


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32))
    password = db.Column(db.String(32))
    full_name = db.Column(db.String(32))
    addresses = db.relationship(Address, backref='user', primaryjoin=user_id == Address.user_id, lazy='joined')
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        include_relationships = True
        load_instance = True
    addresses = fields.Nested(AddressSchema, many=True, allow_none=True)
