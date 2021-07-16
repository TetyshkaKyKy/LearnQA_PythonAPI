from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
from random import choice
from string import ascii_uppercase


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"Users with email '{email}' already exists")

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    data_for_registration_wo_one_param = [
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         'password'),
        ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         'username'),
        ({'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
         'firstName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'vinkotov@example.com'},
         'lastName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}, 'email')
    ]

    @pytest.mark.parametrize("data", data_for_registration_wo_one_param)
    def test_create_user_wo_one_param(self, data):
        data, missed_param = data
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"The following required params are missed: {missed_param}")

    def test_create_user_with_one_symbol_firstName(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': ''.join(choice(ascii_uppercase) for i in range(1)),
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'firstName' field is too short")

    def test_create_user_with_too_long_firstName(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': ''.join(choice(ascii_uppercase) for i in range(251)),
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "The value of 'firstName' field is too long")
