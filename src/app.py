#!/usr/bin/python

from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
import os
from bson.objectid import ObjectId
from bson.json_util import dumps
import config
from db import populate, get_student_names, get_student_data, get_student_rows, get_student_data_grouped

# APP
app = Flask(__name__)
Bootstrap(app)

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))

# Populate DB
populate()


# Calculate email offsets for fetchig lists of emails from MongoDB
def get_navigation_offsets(offset, increment = config.N_PER_PAGE):

    return {
        'Previous': { 'offset': max(offset - increment, 0) }, # Don't go below 0
        'Next': { 'offset': offset + increment },
    }


@app.route('/')
@app.route('/<int:offset>')
def index(offset = 0):

    return render_template('index.html',
                           students=get_student_names(offset),
                           nav_offsets=get_navigation_offsets(offset),
                           nav_path="/")                      


@app.route('/data/<student>')
@app.route('/data/<student>/')
@app.route('/data/<student>/<int:offset>')
def show_transactions(student, offset = 0):

    return render_template('transactions.html',
                           student=student,
                           transactions=get_student_rows(student, offset),
                           nav_offsets=get_navigation_offsets(offset),
                           nav_path="/data/{}/".format(student))


@app.route('/plot/<student>')
@app.route('/plot/<student>/')
def plot(student):

    return render_template('plot.html',
                           student=student,
                           transactions=dumps(get_student_data(student)))


@app.route('/network/<student>')
@app.route('/network/<student>/')
def show_network(student):

    return render_template('network.html',
                           student=student,
                           transactions=dumps(get_student_data(student)))


@app.route('/figures')
@app.route('/figures/')
def show_figures():

    images = []
    figures_path = os.path.join(static_path, "img")

    for name in os.listdir(figures_path):
        path = os.path.join("img", name)
        desc = name.split(".")[0].replace("-", " ").title()
        images.append( dict(name=name, path=path, desc=desc) )

    return render_template('figures.html',
                           images=sorted(images, key=lambda k: k['name']))


@app.route('/figures/<name>')
@app.route('/figures/<name>/')
def show_figure(name):

    path = os.path.join("img", name)
    desc = name.split(".")[0].replace("-", " ").title()
    image = dict(path=path, name=name, desc=desc)

    return render_template('figure.html',
                           image=image)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
