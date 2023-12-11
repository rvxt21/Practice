from scopus import ScopusAPI


def main():
   api = ScopusAPI()
   author_id = '56006224700'
   api.get_author_data(author_id)


if __name__ == "__main__":
   main()
