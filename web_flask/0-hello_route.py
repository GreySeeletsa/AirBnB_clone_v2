#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class
from flask import Flask

# create an instanc: webapp
webapp = Flask(__name__)
webapp.url_map.strict_slashes = False


@webapp.route('/')
def index():
    """To return "Hello HBNB!"
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    webapp.run(debug=True)
