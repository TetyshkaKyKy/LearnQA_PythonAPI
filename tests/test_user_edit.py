import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    # Register & auth of main user
    def setup(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.first_name = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response1, "id")
        self.login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = MyRequests.post("/user/login", data=self.login_data)

        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @allure.description("This test edits user details")
    def test_edit_just_created_user(self):
        new_name = "Changed Name"
        # Edit just created user's name
        response1 = MyRequests.put(f"/user/{self.user_id}",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response1, 200)

        # Check that edit is successful
        response2 = MyRequests.get(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test attempts to edit user details by unauthorized user")
    def test_edit_unauthorized_user(self):
        new_name = "Changed Name Again"

        response = MyRequests.put(f"/user/{self.user_id}",
                                  data={"firstName": new_name}
                                  )
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "Auth token not supplied")

    @allure.description("This test attempts to edit one user by another user")
    def test_edit_one_user_by_another(self):
        # Register 2nd user
        second_user_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=second_user_data)
        second_user_id = self.get_json_value(response1, "id")
        second_username = second_user_data["username"]

        # Edit 2nd user by main user
        new_name = "Second User name"

        response2 = MyRequests.put(f"/user/{second_user_id}",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid},
                                   data={"username": new_name}
                                   )
        Assertions.assert_code_status(response2, 200)

        # Check that name edition failed
        response3 = MyRequests.get(
            f"/user/{second_user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response3,
            "username",
            second_username,
            "Oops!Username was edit by first user!"
        )

    @allure.description("This test attempts to edit user email with incorrect data")
    def test_edit_user_with_incorrect_email(self):
        incorrect_email = "exampleexample.com"
        response = MyRequests.put(f"/user/{self.user_id}",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid},
                                  data={"email": incorrect_email}
                                  )
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, "Invalid email format")

    @allure.description("This test attempts to edit user firstName with incorrect data")
    def test_edit_user_first_name_contains_one_symbol(self):
        new_first_name = 'l'
        response = MyRequests.put(f"/user/{self.user_id}",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid},
                                  data={"firstName": new_first_name}
                                  )

        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            "error",
            "Too short value for field firstName",
            "Oops!Username was edit!"
        )
