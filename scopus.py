import json
from typing import Any

from pybliometrics.scopus import AuthorRetrieval


class ScopusScrapper:

    def __init__(self, author_id: int):
        self.author_id = author_id

    def _search_author_data(self) -> dict:
         au = AuthorRetrieval(author_id=self.author_id)
         author_info = {
             "author_id": self.author_id,
             "url": au.self_link,
             "name": au.surname+" "+au.given_name,
             "affiliation": au.affiliation_current[0].preferred_name,
             "document_count": au.document_count,
             "h_index": au.h_index,
             "citation_count": au.citation_count,
             "documents": au.get_documents(),
             "areas": au.subject_areas,
             "orcid": au.orcid,
             "publication_range": au.publication_range
         }
         return author_info

    @staticmethod
    def _get_author_publications(author_info: dict) -> list[dict[str | Any, Any]]:
        documents = author_info["documents"]
        author_publications = []
        for document in documents:
            author_publication = {
                "eid": document.eid,
                "title": document.title,
                "author_count": document.author_count,
                "author_names": document.author_names,
                "author_ids": document.author_ids,
                "author_afids": document.author_afids,
                "publicationName": document.publicationName,
                "description": document.description,
                "citedby_count": document.citedby_count,
                "authkeywords": document.authkeywords,
                "aggregationType": document.aggregationType,
                "issn": document.issn
            }
            author_publications.append(author_publication)
        return author_publications

    def get_full_author_data(self):
        author_info = self._search_author_data()
        publications_info = self._get_author_publications(author_info=author_info)
        if "documents" in author_info and author_info["documents"]:
            del author_info["documents"]

        full_author_data = {
            "author": author_info,
            "publications": publications_info
        }
        return full_author_data


def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)




