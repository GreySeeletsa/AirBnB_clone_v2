#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class
from flask import Flask

# create an instance called webapp
webapp = Flask(__name__)
webapp.url_map.strict_slashes = False


@webapp.route('/')
def index():
    """To return "Hello HBNB!"
    """
    return 'Hello HBNB!'


@webapp.route('/hbnb')
def hbnb_route():
    """To return "HBNB"
    """
    return 'HBNB'


if __name__ == '__main__':
    webapp.run(debug=True)
