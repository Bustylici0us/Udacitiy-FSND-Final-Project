
import os
import unittest
import json
from flask import Flask
from models import setup_db, Actor, Movie
from app import create_app


CASTING_ASSISTANT = os.getenv('CASTING_ASSISTANT_TOKEN')
CASTING_DIRECTOR = os.getenv('CASTING_DIRECTOR_TOKEN')
EXECUTIVE_PRODUCER = os.getenv('EXECUTIVE_PRODUCER_TOKEN')

class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DATABASE_URL_TEST')
        setup_db(self.app, self.database_path)

        self.new_actor = {'name': 'John Doe', 'age': 30, 'gender': 'Male'}
        self.new_movie = {'title': 'New Movie', 'release_date': '2023-01-01'}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers={"Authorization": f"Bearer {CASTING_ASSISTANT}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers={"Authorization": f"Bearer {CASTING_ASSISTANT}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_actor_casting_director(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": f"Bearer {CASTING_DIRECTOR}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/1', headers={"Authorization": f"Bearer {CASTING_DIRECTOR}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_add_movie_executive_producer(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/1', headers={"Authorization": f"Bearer {EXECUTIVE_PRODUCER}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == "__main__":
    unittest.main()
