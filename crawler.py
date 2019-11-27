import requests

URL_LEETCODE = 'https://leetcode.com/api/problems/algorithms/'
COOKIES_LEETCODE = {'__cfduid': 'd7b27d5500d9b7c41c8e11a7fc9adfa721574730256',
                    '_ga': 'GA1.2.551322794.1574730257',
                    '_gid': 'GA1.2.1205712125.1574730257',
                    'csrftoken': 'jkgetJU8TPni8cPcCVI3PhihhBinfsxJKimvl3y66oQqBf7fpOUV089WpUHDYz3c',
                    'LEETCODE_SESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMzA2OTg4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiYWxsYXV0aC5hY2NvdW50LmF1dGhfYmFja2VuZHMuQXV0aGVudGljYXRpb25CYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjQ4NTEzN2RlMTgyNGRkMzhmNTNjOWVhMjI0YWNlNDA5ZTRhYWRmYyIsImlkIjozMDY5ODgsImVtYWlsIjoic2p0dWZ1aGFvQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiU0pUVUZ1SGFvIiwidXNlcl9zbHVnIjoic2p0dWZ1aGFvIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL3NqdHVmdWhhby9hdmF0YXJfMTU2NjU4NTk3OC5wbmciLCJ0aW1lc3RhbXAiOiIyMDE5LTExLTI3IDAxOjU3OjQ1LjMyNzU4MyswMDowMCIsIklQIjoiMjYwNTplMDAwOjEzMTM6ZDA5NjozOWMyOjU2Mjg6M2E2ZjoxMTA4IiwiSURFTlRJVFkiOiIyYjFmOGRkMzJkNmZlYjgyNmY2MWRhMTFjODcwYjM2ZiIsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.-2P5Malgj4ylEc5JfFPdJXHdCyNa2DP3dVGvJ-C736w'}

class CrawlerLeetcode:
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies
        self.client = requests.session()

    def get_problems_info(self):
        return self.client.get(self.url, cookies=self.cookies).json()

crawlerLeetcode = CrawlerLeetcode(URL_LEETCODE, COOKIES_LEETCODE)