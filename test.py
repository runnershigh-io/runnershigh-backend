import os
import io
import json
import unittest
import tempfile

"""
createdb -O runnershigh_user runnershigh -E utf8 && psql -d runnershigh -c "create extension postgis;" && psql -d runnershigh -f database.sql
"""

class TestBase(unittest.TestCase):

    def setUp(self):
        import runnershigh
        runnershigh.server.config['TESTING'] = True
        runnershigh.server.config['DEBUG'] = True
        self.server = runnershigh.server.test_client()

    def create_user(self, username, password):
        entry_path = '/register/'
        body = dict(roles_id=2, username=username, password=password,
            email = '{0}@email.com'.format(username), location='tucson, az',
            age=25)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.simulate_post(entry_path, data=body, headers=headers)

    def login(self, username, password):
        entry_path = '/login/'
        body = dict(username=username, password=password)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.simulate_post(entry_path, data=body, headers=headers)

    def logout(self):
        entry_path = '/logout/'
        return self.simulate_get(entry_path)

    def delete_user(self, username):
        entry_path = '/users/{0}/'.format(username)
        return self.simulate_delete(entry_path)

    def simulate_get(self, path, **kwargs):
        return self.server.get(path, **kwargs)

    def simulate_post(self, path, **kwargs):
        return self.server.post(path, **kwargs)

    def simulate_delete(self, path, **kwargs):
        return self.server.delete(path, **kwargs)

    def simulate_put(self, path, **kwargs):
        return self.server.put(path, **kwargs)


class TestAuth(TestBase):

    def test_auth(self):
        response = self.create_user('user1', 'password1')
        assert response.status_code == 201
        response = self.login('user1', 'password1')
        assert response.status_code == 200
        response = self.logout()
        assert response.status_code == 200
        self.login('user1', 'password1')
        response = self.delete_user('user1')
        assert response.status_code == 200


class TestUser(TestBase):

    def _get_user(self):
        entry_path = '/users/{0}/'.format(self.username)
        return self.simulate_get(entry_path)

    def _update_user(self):
        entry_path = '/users/{0}/'.format(self.username)
        body = dict(roles_id=2, username='new_user', password='password',
            email = 'new_user@email.com', location='arizona')
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.simulate_put(entry_path, data=body, headers=headers)

    def _delete_user(self):
        return self.delete_user(self.username)

    def test_user_fail(self):
        self.create_user('user1', 'password1')
        self.create_user('user2', 'password2')
        self.username = 'user2'
        self.password = 'password2'
        response = self._get_user()
        assert response.status_code == 403
        self.login('user1', 'password1')
        response = self._update_user()
        assert response.status_code == 401
        response = self._delete_user()
        assert response.status_code == 401
        #clean-up
        self.username = 'user1'
        self.password = 'password1'
        self._delete_user()
        self.login('user2', 'password2')
        self.username = 'user2'
        self.password = 'password2'
        self._delete_user()

    def test_user_pass(self):
        self.username = 'user3'
        self.password = 'password3'
        self.create_user(self.username, self.password)
        self.login(self.username, self.password)
        response = self._get_user()
        assert response.status_code == 200
        response = self._update_user()
        assert response.status_code == 200
        self.username = 'new_user'
        self.password = 'password'
        response = self._delete_user()
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
