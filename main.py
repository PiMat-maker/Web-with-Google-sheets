from database.creating_database import create_db
from google_sheets.data_uploader import upload_sheets_data


def main():
    sheets_data = upload_sheets_data()
    create_db()


if __name__ == "__main__":
    main()