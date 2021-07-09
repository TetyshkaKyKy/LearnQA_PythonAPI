from requests import Response
import json
import json.decoder

class Assertions:
    #Класс не является прямым наследником для наших тестов, чтобы использовать функции этого класса - делаем функции статическими
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key'{name}'"
        assert response_as_dict[name] == expected_value, error_message

