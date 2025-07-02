from extract import extract
from transform import transform
from load import load

def main():
    print("Starting ETL Pipeline")

    extract()
    transform()
    load()

    print(" ETL Pipeline completed successfully")

if __name__ == "__main__":
    main()