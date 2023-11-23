from scholar_api import ScholarAPI
import json


def save_to_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def main():
    api = ScholarAPI()

    author_id = "1692601414"
    author_info = api.get_author_info(author_id=author_id)

    if author_info:
        papers_info = api.get_author_papers_info(author_id, author_info)
        file_name = f"{author_info['name']}_data.json"
        file_p_name = f"{author_info['name']}_papers_data.json"

        save_to_json(file_name, {"author_info": author_info})
        save_to_json(file_p_name, {"papers_info": papers_info})

        print(f"Дані про автора збережено у файлі: {file_name}")
        print(f"Дані про публікації збережено у файлі: {file_p_name}")


if __name__ == "__main__":
    main()