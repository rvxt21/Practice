import json
from typing import Any
import pandas as pd


class SemanticScholarToExcel:
    def __init__(self, file_name):
        self.file_name = file_name

    def _open_json_file(self, file_name):
        with open(self.file_name, "r", encoding="utf-8") as file:
            json_data = json.load(file)
        return json_data

    @staticmethod
    def _write_author_data(json_data) -> dict:
        author_info = json_data["author"]
        author_data = {
            "Author URL": [author_info["url"]],
            "Author Name": [author_info["name"]],
            "Author Paper Count": [author_info["paperCount"]],
            "Author hIndex": [author_info["hIndex"]]
        }
        return author_data

    @staticmethod
    def _write_publications_data(json_data) -> list[dict[str, str | None | Any]]:
        publications_info = json_data["publications"]["data"]
        publications_data = []

        for publication in publications_info:
            publication_data = {
                "Publication URL": publication["url"],
                "Назва публікації": publication["title"],
                "Рік публікації": publication["year"],
                "Кількість цитувань": publication["citationCount"],
                "Галузі навчання": ', '.join(publication["fieldsOfStudy"]) if
                publication["fieldsOfStudy"] else None,
                "S2 Fields of Study": ', '.join(fos["category"] for fos
                                                in publication[
                                                    "s2FieldsOfStudy"]) if
                publication["s2FieldsOfStudy"] else None,
                "Дата публікації": publication["publicationDate"]
            }

            authors = [author["name"] for author in publication["authors"]]
            publication_data["Authors"] = ', '.join(
                authors) if authors else None

            publications_data.append(publication_data)

        return publications_data

    def _create_and_save_excel_file(self,author_data: dict, publications_data: list[
        dict[str, str | None | Any]]):
        excel_file_path = f"semantic_scholar_excels/{self.file_name.split('semantic_scholars_jsons/')[1].split('.json')[0]}.xlsx"
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            author_df = pd.DataFrame(author_data)
            author_df.to_excel(writer, sheet_name='Author', index=False)

            publications_df = pd.DataFrame(publications_data)
            publications_df.to_excel(writer, sheet_name='Publications',
                                     index=False)

    def get_authors_report(self, file_name:str):
        json_data = self._open_json_file(file_name=file_name)
        author_data = self._write_author_data(json_data=json_data)
        publications_data = self._write_publications_data(json_data=json_data)
        self._create_and_save_excel_file(author_data=author_data,
                                     publications_data=publications_data)
        print(f"Saved_to: {file_name.split('semantic_scholars_jsons/')[1].split('.json')[0]}.xlsx")


def main():
    file_name = "semantic_scholars_jsons/Semantic_Scholar_O. Gnedkova_data.json"
    s = SemanticScholarToExcel(file_name)
    s.get_authors_report(file_name=file_name)


if __name__ == "__main__":
    main()