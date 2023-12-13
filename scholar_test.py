from scholar_api import SemanticScholarScrapper
import json
import time


def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def main():
    author_id = "143987284"
    ss = SemanticScholarScrapper(author_id)
    author_info = ss.get_full_author_data()

    if author_info:
        file_name = f"semantic_scholars_jsons/Semantic_Scholar_{author_info['author']['name']}_data.json"
        save_to_json(file_name, author_info)

        print(f"Всі дані про автора збережено у файлі: {file_name}")


if __name__ == "__main__":
    main()