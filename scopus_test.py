from scopus import ScopusScrapper,save_to_json


def main():
   scrapper = ScopusScrapper(16431204200)
   full_author_data = scrapper.get_full_author_data()
   if full_author_data:
      file_name = f"scopus_jsons/Scopus_{full_author_data['author']['name']}_data.json"
      save_to_json(file_name, full_author_data)

      print(f"Всі дані про автора збережено у файлі: {file_name}")


if __name__ == "__main__":
   main()
