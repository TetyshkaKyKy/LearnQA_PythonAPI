from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_unauthorized_users_details(self):
        response = MyRequests.get("/user/2")

        field_list_not_in_response = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, field_list_not_in_response)

    def setup(self):
        # Auth of main user
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_user_gets_his_user_details(self):
        response = MyRequests.get(
            f"/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response, expected_fields)

    def test_authorized_user_gets_user_details_another_user(self):
        response = MyRequests.get(
            "/user/1",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        field_list_not_in_response = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, field_list_not_in_response)
