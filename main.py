"""
Server file module
"""

from flask import render_template

# local modules
import config


# Get the application instance
from seed_database import init_database

connex_app = config.connex_app

# Read the users_api.yml file to configure the endpoints
connex_app.add_api("users_api.yml")

if __name__ == "__main__":
    init_database()
    connex_app.run(debug=True, host='127.0.0.1')
