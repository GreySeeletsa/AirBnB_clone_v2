#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class from flask module render_template for rendering templates
from flask import Flask, render_template
from models import storage

# create an instance called webapp
webapp = Flask(__name__)
webapp.url_map.strict_slashes = False


@webapp.teardown_appcontext
def teardown_db(exception=None):
    """removes the current SQLAlchemy Session
    """
    if storage is not None:
        storage.close()


@webapp.route('/states_list')
def states_list(n=None):
    """displays a HTML page"""
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    webapp.run(debug=True)
