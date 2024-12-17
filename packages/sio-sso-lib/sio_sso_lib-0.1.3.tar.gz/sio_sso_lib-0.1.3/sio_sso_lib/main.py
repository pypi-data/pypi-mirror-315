import requests

class ssoAuthentification:
    def __init__(self):
        self.API_URL = "https://sso.inoctet.fr/"

    def verifyToken(self, token: str):
        """
            Public method to verify token validity, if it is, return user Data

            Response:
                -> Bool if request is valid
                -> Object?
        """
        try:
            api_response = requests.get(self.API_URL + "auth/session", {
                'token': token,
                'extra': 'true'
            })

            if api_response and api_response['status']:
                return [True, api_response['details']]
        except:
            pass

        return [False, {}]

