class APIException(Exception):
    def __init__(self, response):
        super(APIException, self).__init__()

        self.code = 0

        try:
            json_response = response.json()
        except ValueError:
            self.message = "JSON error message: {}".format(response.text)
        else:
            if "error" not in json_response:
                self.message = "Wrong json format from API"
            else:
                self.message = json_response["error"]

        self.status_code = response.status_code
        self.response = response

    def __str__(self):
        return "APIException(status_code: {}): {}".format(self.status_code, self.message)


class RequestException(Exception):
    def __init__(self, message):
        super(RequestException, self).__init__()
        self.message = message

    def __str__(self):
        return "RequestException: {}".format(self.message)