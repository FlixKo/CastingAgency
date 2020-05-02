import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime
import random
import dateutil.parser
import babel

from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth

#def create_app(test_config=None):
    # create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = "super secret key"
setup_db(app)

CORS(app)

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

'''
MOVIES
'''

'''
@:
Create an endpoint to handle GET requests
for all available movies.
'''
@app.route("/movies", methods=['GET'])
# @cross_origin()
def get_movies():
    movies = Movie.query.all()

    if len(movies) == 0:
        abort(404)

    data = []
    for movie in movies:
        data.append(movie.format())

    return jsonify({
        'success': True,
        'movies': data,
        'total_movies': len(movies)
    })

'''
@:
Create an endpoint to DELETE movie using a movie ID.

'''

@app.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth('delete:movies')
# @cross_origin()
def delete_movie(payload, movie_id):

    try:
        Movie.query.filter(Movie.id == movie_id).one_or_none().delete()

        return jsonify({
            'success': True,
            'message': "Movie successfully deleted.",
            'deleted': movie_id
        })
    except BaseException:
        abort(404)

'''
@:
Create an endpoint to POST a new movie,
which will require its title and release date.

'''

@app.route("/movies", methods=['POST'])
@requires_auth('post:movies')
# @cross_origin()
def add_movie(payload):
    try:
        new_movie = Movie(
            title="Test Title 3",
            releaseDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        new_movie.insert()

        return jsonify({
            'success': True,
            'movies': new_movie.format(),
            'created': new_movie.id,
            'total_movies': len(Movie.query.all())
        })
    except AuthError:
        abort(422)

'''
edit existing movie
'''
@app.route("/movies/<int:movie_id>", methods=['PATCH'])
@requires_auth('patch:movies')
# @cross_origin()
def edit_movie(payload, movie_id):
    try:
        title_update = 'Updated Title'
        release_date_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if update_movie is None:
            abort(404)

        update_movie.title = title_update
        update_movie.releaseDate = release_date_update

        update_movie.update()

        return jsonify({
            'success': True,
            'movies': update_movie.format(),
            'total_movies': len(Movie.query.all())
        })
    except AuthError:
        abort(422)

'''
ACTORS
'''

'''
@:
Create an endpoint to handle GET requests
for all available actors.
'''
@app.route("/actors", methods=['GET'])
# @cross_origin()
def get_actors():
    actors = Actor.query.all()

    if len(actors) == 0:
        abort(404)

    data = []
    for actor in actors:
        data.append(actor.format())

    return jsonify({
        'success': True,
        'actors': data,
        'total_actors': len(actors)
    })

'''
@:
Create an endpoint to DELETE actor using a actor ID.

'''

@app.route("/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth('delete:actors')
# @cross_origin()
def delete_actor(payload, actor_id):

    try:
        Actor.query.filter(Actor.id == actor_id).one_or_none().delete()

        return jsonify({
            'success': True,
            'message': "Actor successfully deleted.",
            'deleted': actor_id
        })
    except BaseException:
        abort(404)

'''
@:
Create an endpoint to POST a new actor,
which will require its name, age and gender.

'''

@app.route("/actors", methods=['POST'])
@requires_auth('post:actor')
# @cross_origin()
def add_actor(payload):
    try:
        new_actor = Actor(
            name="Hugo",
            age=42,
            gender="M"
        )

        new_actor.insert()

        return jsonify({
            'success': True,
            'actors': new_actor.format(),
            'created': new_actor.id,
            'total_actors': len(Actor.query.all())
        })
    except AuthError:
        abort(422)

'''
edit existing actor
'''
@app.route("/actors/<int:actor_id>", methods=['PATCH'])
@requires_auth('patch:actors')
# @cross_origin()
def edit_actor(payload, actor_id):
    try:
        name_update = 'Updated Name'
        age_update = 34
        gender_update = "F"
        update_actor = Actor.query.filter(
            Actor.id == actor_id).one_or_none()

        if update_actor is None:
            abort(404)

        update_actor.name = name_update
        update_actor.age = age_update
        update_actor.gender = gender_update

        update_actor.update()

        return jsonify({
            'success': True,
            'actors': update_actor.format(),
            'total_actors': len(Actor.query.all())
        })
    except AuthError:
        abort(422)

'''
Error handlers for all expected errors

'''
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404

@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Sent instructions are unprocessable"
    }), 422

@app.errorhandler(AuthError)
def invalid_claims(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.__dict__
    }), 401

    #return app
