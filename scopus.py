import requests


class ScopusAPI:
    def __init__(self):
        self.base_url = 'https://www.scopus.com/api/'

    def get_author_data(self,author_id: str):
        author_url= f'{self.base_url}authors/{author_id}'
        response = requests.get(author_url)

        if response.status_code == 200:
            author_data = response.json()
            print(author_data)
        else:
            print(f"Error: {response.status_code}")
            return None
