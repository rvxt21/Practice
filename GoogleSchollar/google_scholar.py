import json

import requests
params = {
  "engine": "google_scholar_author",
  "author_id": "",
  "api_key": "ac547c17d6148634622dd68414ed1964333f0b582ed2665e68710b2d7b5d2591"
}


class GoogleScholarParser:

    def __init__(self, author_id: str):
        self.author_id = author_id
        self.author_url = f"https://serpapi.com/search.json?engine=google_scholar_author&api_key={params['api_key']}&author_id={self.author_id}"

    def get_author_info(self):
        response = requests.get(self.author_url)
        if response.status_code == 200:
            author_data = response.json()
            serpapi_pagination = author_data.get("serpapi_pagination", {})
            next_url = serpapi_pagination.get("next") + f"&api_key={params['api_key']}"

            while next_url:
                next_page_publications_response = requests.get(next_url)
                if next_page_publications_response.status_code == 200:
                    next_page_data = next_page_publications_response.json()
                    updated_articles_data = author_data.get('articles', [])
                    updated_articles_data.extend(
                        next_page_data.get('articles', []))
                    updated_serpapi_pagination = next_page_data.get(
                        'serpapi_pagination', {})
                    next_url = updated_serpapi_pagination.get('next')
                    if next_url is not None:
                        next_url += f"&api_key={params['api_key']}"

                    author_data['articles'] = updated_articles_data
                    author_data['serpapi_pagination']['next'] = next_url

                    # Збереження серіалізованих даних про автора в файл
                    file_name = f"googlescholar_jsons/GoogleScholar_{author_data.get('author', {}).get('name', '').split('/')[0]}_data.json"
                    self._save_to_json(file_name, author_data)

                else:
                    print(
                        f"Error fetching next page data: {next_page_publications_response.status_code}")
                    break

            return author_data

    @staticmethod
    def _save_to_json(file_name, data):
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    au = GoogleScholarParser("EjLwtBoAAAAJ")
    au.get_author_info()
