from typing import List

import requests


class WebOfScienceParser:
    def __init__(self):
        self.wos_session_id = 'EUW1ED0E6EZycnWie8ept6N1RlHoV'
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'X-1P-WOS-SID': self.wos_session_id,
        }

    def get_user_full_info(self, author_id: int)-> dict:
        author_info = self._get_author_info(author_id)
        author_rid = author_info['Data']['Records'][0]['rid']
        author_publications = self._get_author_publications(author_rid)
        return {'author': author_info,
                'publications': author_publications}

    def _get_author_info(self, author_id: int) -> dict:
        data = {
            "search": {
                "mode": "author_id",
                "database": "AUTHOR",
                "authorId": {
                    "type": "spid",
                    "value": author_id
                }
            },
            "retrieve": {
                "Count": "1",
                "FirstRecord": "1",
                "Options": {
                    "View": "AuthorFullDetail",
                    "DataFormat": "Map",
                    "ReturnType": "List",
                    "RemoveQuery": "On"
                }
            }
        }
        url = 'https://www.webofscience.com/api/esti/SearchEngine/search'
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def _get_author_publications(self, rid: str) -> List[dict]:
        pubs = []
        url = f'https://www.webofscience.com/wos-researcher/profile/publication/{rid}/?order_by=date-published&page=1&per_page=25'
        while url:
            content = requests.get(url, headers=self.headers).json()
            pubs.extend(content.get('results'))
            url = content.get('next')
        return pubs

if __name__ == '__main__':
    wosp = WebOfScienceParser()
    print(wosp.get_user_full_info(1046766))

