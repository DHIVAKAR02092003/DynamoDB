from extract import extract
from load import load
from transform import transform 

if __name__ == "__main__" : 
    raw_data = extract()
    print("Data Extraction was done Successfully...")
    df1, df2 = transform(raw_data)
    print("Transformation done successfully...")
    load(df1, df2)
    print("ETL Process completed.")