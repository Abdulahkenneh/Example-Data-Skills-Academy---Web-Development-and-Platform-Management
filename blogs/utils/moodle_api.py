# # myapp/utils/moodle_api.py

# import requests

# class MoodleAPI:
#     def __init__(self, url, token):
#         self.url = url.rstrip('/')
#         self.token = token

#     def call(self, wsfunction, params=None):
#         params = params or {}
#         params.update({
#             'wstoken': self.token,
#             'moodlewsrestformat': 'json',
#             'wsfunction': wsfunction,
#         })
#         response = requests.post(f'{self.url}/webservice/rest/server.php', params=params)
#         return response.json()
