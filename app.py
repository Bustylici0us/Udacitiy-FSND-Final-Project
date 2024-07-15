from flask import Flask, request, jsonify, abort
from models import setup_db, Movie, Actor, db_drop_and_create_all
from flask_cors import CORS
from authorization import requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
with app.app_context():
    db_drop_and_create_all()

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if not body:
            abort(400)
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        if not title or not release_date:
            abort(400)
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if not body:
            abort(400)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if not name or not age or not gender:
            abort(400)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        body = request.get_json()
        movie.title = body.get('title', movie.title)
        movie.release_date = body.get('release_date', movie.release_date)
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        body = request.get_json()
        actor.name = body.get('name', actor.name)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'delete': movie_id
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            'delete': actor_id
        })

    if __name__ == '__main__':
        app.run()
