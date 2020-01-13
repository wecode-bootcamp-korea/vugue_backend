import json
import bcrypt
import unittest

from datetime      import datetime
from .models       import User
from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

class UserTest(unittest.TestCase):
    def setUp(self):
        hashed_password = bcrypt.hashpw('12345'.encode('utf-8'),bcrypt.gensalt())

        User.objects.create(
                name = 'yerin',
                password = hashed_password.decode('utf-8'), 
                )

    def tearDown(self):
        User.objects.get(name='yerin').delete()

    def test_signup(self):
        test = {
                'name':'jinju',
                'password':'123456',
                }
        response = Client().post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_same_name(self):
        test = {
                'name':'yerin',
                'password':'12345',
                }
        response = Client().post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message":"NAME_ALREADY_EXIST"})

    def test_signup_keyerror(self):
        test = {
                'nam':'jj',
                'password':'222333',
                }
        response = Client().post('/user', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_KEYS"})

    def test_signin(self):
        test = {
                'name':'yerin',
                'password':'12345',
                }
        response = Client().post('/user/auth', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"access_token": response.json()["access_token"]})

    def test_signin_no_user(self):
        test = {
                'name':'kamil',
                'password':'333444',
                }
        response = Client().post('/user/auth', json.dumps(test), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{"message":"INVALID_USER"})
    
    def test_signin_keyerror(self):
        test = {
                'nam':'kk',
                'password':'234234',
                }
        response = Client().post('/user/auth', json.dumps(test), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_KEYS"})


    @patch('user.views.requests')
    def test_kakao_login(self, mocked_requests):
        c = Client()

        class FakeResponse:
            def json(self):
                return{
                        "id":"99"
                        }
            mocked_requests.get = MagicMock(return_value = FakeResponse())
            header = {'HTTP_Authorization':'1234abcd'}
            response = c.get('/user/kakao_signin', content_type ='application/json', **header)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
