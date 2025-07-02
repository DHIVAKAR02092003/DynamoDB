from sqlalchemy import create_engine
from configparser import ConfigParser
from urllib.parse import quote_plus
from pathlib import Path

def load(df1, df2):
    config = ConfigParser()
    config.read(Path(__file__).parent.parent / "config" / "config.ini")

    server = config['sqlserver']['server']
    database = config['sqlserver']['database']
    username = config['sqlserver']['username']
    password = config['sqlserver']['password']
    driver = config['sqlserver']['driver']

    password = quote_plus(password)   #for encoding the special chars
    driver = quote_plus(driver)

    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
    engine = create_engine(connection_string)

    df1.to_sql('Projects', con=engine, if_exists='replace', index=False)
    df2.to_sql('ProjectTechnologies', con=engine, if_exists='replace', index=False)

    print(" Data inserted successfully...")
