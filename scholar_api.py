import requests
from pprint import pprint

class ScholarAPI:

    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"

    def get_author_info(self, author_id: int):
        fields = "authorId,url,name,aliases,affiliations,homepage,paperCount,citationCount,hIndex"
        author_url = f"{self.base_url}/author/{author_id}?fields={fields}"
        response = requests.get(author_url)

        if response.status_code == 200:
            author_data = response.json()
            return self.extract_author_info(author_data)
        else:
            print(f"Error: {response.status_code}")
            return None

    def extract_author_info(self, author_data) -> dict:
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

    def get_author_papers_info(self, author_id: int, author_info):
        fields = "paperId,corpusId,url,title,abstract,venue,publicationVenue," \
                 "year,referenceCount,citationCount,influentialCitationCount," \
                 "isOpenAccess,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy," \
                 "publicationTypes,publicationDate,journal,authors,citations," \
                 "authors,references"
        author_papers_url = f"{self.base_url}/author/{author_id}/papers?fields={fields}"
        response = requests.get(author_papers_url)

        if response.status_code == 200:
            author_papers_info = response.json()
            pprint(author_papers_info)
            return author_papers_info
        else:
            print(f"Error: {response.status_code}")
            return None