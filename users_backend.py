"""
This is the users module and supports all the REST actions for the
users data
"""
from connexion import full_name
from flask import make_response, abort
from config import db
from models.address import AddressSchema, Address
from models.user import User, UserSchema


def list_all(page, per_page):
    """
    Responds to a request for /users
    with the complete lists of users
    :return:        json string of list of users
    """
    # Create the list of users from our data
    users = User.query.order_by(User.full_name).paginate(page, per_page, error_out=False)
    # users = User.query.order_by(User.full_name).all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True, exclude=["password"])
    data = user_schema.dump(users.items)
    return data


def user_detail(id):
    """
    This function responds to a request for /users/{id}
    with one matching user from users
    :param id:   Id of user to find
    :return:     user matching id
    """
    # Get the user requested
    user = User.query.filter(User.user_id == id).one_or_none()

    # Did we find a user?
    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema(exclude=["password"])
        data = user_schema.dump(user)
        return data

    # Otherwise, nope, didn't find that user
    else:
        abort(
            404,
            "User not found for Id: {id}".format(user_id=id),
        )


def create(user_candidate):
    """
    Creates a new user in the users structure
    based on the passed in user data
    :param user_candidate:  user candidate to create in users structure
    :return:        201 on success, 406 on user exists
    """

    email = user_candidate.get("email")

    # Validate if user exists
    existing_user = (
        User.query #.filter(User.full_name == full_name)
        .filter(User.email == email)
        .one_or_none()
    )

    if existing_user is None:

        # Create a user instance using the schema and the passed in user
        schema = UserSchema()
        new_user = schema.load(user_candidate, session=db.session)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_user)

        return data, 201

    # Otherwise, user already exists
    else:
        abort(
            409,
            "User {full_name}  already exists".format(
                full_name=full_name
            ),
        )


def create_address(id, address_candidate):
    """
    Creates a new user address in the users structure
    based on the passed in user data
    :param id:   Id of user to find
    :param address_candidate:  user candidate to create in users structure
    :return:        201 on success, 406 on user exists, 409 user doesn't exists
    """

    # Validate if user exists
    existing_user = (
        User.query.filter(User.user_id == id)
        .one_or_none()
    )

    # Can we insert an address to this user?
    if existing_user:
        if len(existing_user.addresses) > 2:
            abort(
                # 406 Not Acceptable
                406,
                "User id {id} already reached the maximum addresses allowed".format(
                    id=id
                ),
            )

        # Create a user instance using the schema and the passed in user
        schema = AddressSchema()
        new_address = schema.load(address_candidate, session=db.session)

        if len(existing_user.addresses) == 0:
            new_address.primary_address = True
        else:
            new_address.primary_address = False

        # Add the address to the user in the database
        existing_user.addresses.append(new_address)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_address)

        return data, 201

    # Otherwise, user already exists
    else:
        abort(
            409,
            "User id {id} does not exists".format(
                user_id=id
            ),
        )


def update_primary_addresss(id, primary_id):
    """
    Replace the address desired to default
    :param id:   Id of user to find
    :param primary_id:  Id of address
    :return:        200 on success, 404 user not found
    """

    # Validate if user exists
    existing_user = (
        User.query.filter(User.user_id == id)
            .one_or_none()
    )
    if existing_user:
        user_addresses = Address.query.filter(Address.user_id == id)
        new_primary_address = Address.query\
            .filter(Address.user_id == id)\
            .filter(Address.address_id == primary_id).one_or_none()

        if new_primary_address is None:
            abort(
                404,
                "Address Id {primary_id} not found for User Id: {id}".format(primary_id=primary_id, id=id),
            )
        for address in user_addresses:
            address.primary_address = False
        new_primary_address.primary_address = True
        db.session.commit()

        # Serialize and return the updated address in the response
        schema = AddressSchema()
        data = schema.dump(new_primary_address)
        return data, 200


def update_password(id, new_password):
    """
    This function updates an existing user in the users structure
    Throws an error if a user with the name we want to update to
    already exists in the database.
    :param id:   Id of the user to update in the users structure
    :param new_password: Password to replace
    :return:      updated user structure for password
    """

    if new_password == '':
        abort(
            400,  # 400 Bad request (bad parameter)
            "New Password value must be not empty"
            )

    # Validate if user exists
    existing_user = (
        User.query.filter(User.user_id == id)
            .one_or_none()
    )

    # Can we insert an address to this user?
    if existing_user is None:
        abort(
            404,
            "User not found for Id: {id}".format(id=id),
        )

    existing_user.password = new_password
    db.session.commit()

    return "Password for user Id {id} successfully changed".format(id=id), 200

