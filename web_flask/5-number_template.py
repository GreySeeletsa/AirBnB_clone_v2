#!/usr/bin/python3
"""script that starts a Flask web application"""


# import Flask class, and render_template
from flask import Flask, render_template

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


@webapp.route('/c/<text>')
def routefor_C(text):
    """display "C", followed by the value of the text variable
    """
    return 'C {}'.format(text.replace('_', ' '))


@webapp.route('/python', defaults={'text': 'is cool'})
@webapp.route('/python/<text>')
def python_route(text):
    """display "Python", followed by the value of the text variable
    """
    return 'Python {}'.format(text.replace('_', ' '))


@webapp.route('/number/<int:n>')
def number_route(n):
    """display "n is a number" only if n is an integer
    """
    return '{} is a number'.format(n)


@webapp.route('/number_template/<int:n>')
def number_template_route(n):
    """display a HTML page only if n is an integer
    """
    return render_template('5-number.html', num=n)


if __name__ == '__main__':
    webapp.run(debug=True)
