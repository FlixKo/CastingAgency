import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flaskr import create_app
from models import setup_db, Movie, Actor
from flask_cors import CORS, cross_origin


class CastingAgency(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = 'postgres://ubuntu:ubuntu@localhost:5432/' + self.database_name
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'Test Movie Title',
            'releaseDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.new_actor = {
            'name': 'Test Name',
            'age': 34,
            'gender': 'M'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_movie(self):
        res = self.client().post('/movie', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_post_actor(self):
        res = self.client().post('/actor', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_movie(self):
        res = self.client().delete('/movie/1')
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor(self):
        res = self.client().delete('/actor/1')
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_404_no_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_404_no_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
