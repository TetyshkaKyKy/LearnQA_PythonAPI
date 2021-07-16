import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Delete cases")
class TestUserDelete(BaseCase):
    # Register & auth of main user
    def setup(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.user_id = self.get_json_value(response1, "id")
        self.password = register_data["password"]
        self.email = register_data["email"]
        self.login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post("/user/login", data=self.login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.description("This test attempts to delete superuser ")
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_content(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test attempts to delete one user by another user")
    def test_delete_user_by_other_user(self):
        # Register new user
        new_user = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=new_user)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        new_user_user_id = self.get_json_value(response1, "id")
        new_username = new_user["username"]

        # Attempt to delete new user by main user
        response2 = MyRequests.delete(f"/user/{new_user_user_id}",
                                      headers={"x-csrf-token": self.token},
                                      cookies={"auth_sid": self.auth_sid},
                                      )
        Assertions.assert_code_status(response2, 200)

        # Check that attempt is failed (new user is not deleted)
        response3 = MyRequests.get(f"/user/{new_user_user_id}",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid},
                                   )
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(
            response3,
            "username",
            new_username,
            "Wrong user name!"
        )

    @allure.description("This test deletes user")
    def test_delete_user_by_himself(self):
        # Delete user by himself
        response1 = MyRequests.delete(f"/user/{self.user_id}",
                                      headers={"x-csrf-token": self.token},
                                      cookies={"auth_sid": self.auth_sid},
                                      )
        Assertions.assert_code_status(response1, 200)

        # Check that user is deleted
        response2 = MyRequests.get(f"/user/{self.user_id}",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid},
                                   )
        Assertions.assert_code_status(response2, 404)
        Assertions.assert_content(response2, "User not found")
