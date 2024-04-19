import unittest
from api import app
from models.state import State
from models import storage


class TestAPI(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_states(self):
        state = State(name="Test State")
        state.save()
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test State', response.data)

    def test_get_state(self):
        state = State(name="Test State")
        state.save()
        response = self.app.get(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test State', response.data)

    def test_delete_state(self):
        state = State(name="Test State")
        state.save()
        response = self.app.delete(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(State, state.id), None)

    def test_create_state(self):
        response = self.app.post('/api/v1/states',
                                 json={'name': 'New State'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'New State', response.data)

    def test_update_state(self):
        state = State(name="Test State")
        state.save()
        response = self.app.put(f'/api/v1/states/{state.id}',
                                json={'name': 'Updated State'})
        self.assertEqual(response.status_code, 200)
        updated_state = storage.get(State, state.id)
        self.assertEqual(updated_state.name, 'Updated State')

    def tearDown(self):
        for state in storage.all(State).values():
            storage.delete(state)
        storage.save()


if __name__ == '__main__':
    unittest.main()
