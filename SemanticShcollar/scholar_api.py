from typing import Any
import inspect
import requests
import json


class SemanticScholarScrapper:
    def __init__(self, author_id):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.author_id = author_id

    def _get_author_info(self):
        fields = "authorId,url,name,aliases,affiliations,homepage,paperCount," \
                 "citationCount,hIndex"
        author_url = f"{self.base_url}/author/{self.author_id}?fields={fields}"

        response = requests.get(author_url)

        if response.status_code == 200:
            author_data = response.json()
            return self._extract_author_info(author_data)
        elif response.status_code == 400:
            print(f"Error {response.status_code}: Bad query parameters")
            status_code = response.status_code
            error_message = 'Bad query parameters'
            self._update_to_error_json(status_code=status_code,
                                       error_message=error_message)
        elif response.status_code == 404:
            print(f"Error {response.status_code}: Bad paper id")
            status_code = response.status_code
            error_message = ' Bad paper id'
            self._update_to_error_json(status_code=status_code,
                                       error_message=error_message)

    def _extract_author_info(self, author_data) -> dict:
        author_info = {
            "authorId": author_data.get("authorId"),
            "url": author_data.get("url"),
            "name": author_data.get("name"),
            "aliases": author_data.get("aliases"),
            "affiliations": author_data.get("affiliations"),
            "homepage": author_data.get("homepage"),
            "paperCount": author_data.get("paperCount"),
            "citationCount": author_data.get("citationCount"),
            "hIndex": author_data.get("hIndex"),
            "publications": author_data.get("papers")
        }
        return author_info

    def _get_author_papers_info(self):
        fields = "paperId,corpusId,url,title,abstract,venue,publicationVenue," \
                 "year,referenceCount,citationCount,influentialCitationCount," \
                 "isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy," \
                 "publicationTypes,publicationDate,journal,authors,citations," \
                 "references"
        author_papers_url = f"{self.base_url}/author/{self.author_id}/papers?fields={fields}"
        response = requests.get(author_papers_url)

        if response.status_code == 200:
            author_papers_info = response.json()
            return author_papers_info
        elif response.status_code == 400:
            print(f"Error {response.status_code}: Bad query parameters")
            status_code = response.status_code
            error_message = 'Bad query parameters'
            self._update_to_error_json(status_code=status_code,
                                       error_message=error_message)

    def get_full_author_data(self):
        author_info = self._get_author_info()
        if author_info:
            author_papers_info = self._get_author_papers_info()
            full_author_data = {
                "author": author_info,
                "publications": author_papers_info
            }
            return full_author_data
        return None

    @staticmethod
    def _open_template_json_file():
        with open('template.json', 'r', encoding='utf-8') as template_file:
            template_data = json.load(template_file)
        return template_data

    @staticmethod
    def _save_to_json(file_name: Any, data: Any) -> None:
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

    def _update_to_error_json(self, status_code: int, error_message: str):
        template_data = self._open_template_json_file()
        stack = inspect.stack()
        for frame in stack:
            if frame.function == '_get_author_info':
                if 'error' not in template_data['author']:
                    template_data['author']['error'] = {}
                template_data['author']['error']['status code'] = status_code
                template_data['author']['error']['message'] = error_message
            elif frame.function == '_get_author_papers_info':
                if 'error' not in template_data['publications']:
                    template_data['publications']['error'] = {}
                template_data['publications']['error']['status code'] = status_code
                template_data['publications']['error']['message'] = error_message

        file_name = f"Error{self.author_id}_data.json"
        self._save_to_json(file_name, template_data)