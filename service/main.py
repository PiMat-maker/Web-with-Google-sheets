from database.creating_database import create_db, Order
from google_sheets.data_uploader import upload_sheets_data


def main():
    sheets_data = upload_sheets_data()
    print("Uploaded")
    create_db()
    print("Created")
    print(Order.__dir__)


if __name__ == "__main__":
    main()