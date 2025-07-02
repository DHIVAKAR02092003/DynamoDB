import json
import pyodbc
import configparser
import os

def load():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.ini')
    config.read(config_path)

    server = config['sqlserver']['server']
    database = config['sqlserver']['database']
    username = config['sqlserver']['username']
    password = config['sqlserver']['password']
    driver = config['sqlserver']['driver']

    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = conn.cursor()

    # Creating tables if not exist to avoid previous work disturbance
    cursor.execute("""
    If not exists (
        Select * from INFORMATION_SCHEMA.TABLES Where TABLE_NAME = 'Projects'
    )
    BEGIN
        Create Projects (
            project_id VARCHAR(50) PRIMARY KEY,
            project_name VARCHAR(255),
            client VARCHAR(255),
            domain VARCHAR(100),
            location VARCHAR(100),
            project_manager VARCHAR(100),
            start_date DATE,
            end_date DATE,
            status VARCHAR(50)
        )
    END
    """)

    cursor.execute("""
    If Not Exists (
        Select * From INFORMATION_SCHEMA.TABLES Where TABLE_NAME = 'ProjectTechnologies'
    )
    BEGIN
        Create Table ProjectTechnologies (
            project_id varchar(50),
            technology varchar(100),
            PRIMARY KEY (project_id, technology)
        )
    END
    """)
    conn.commit()

    # Loading the projects
    with open('transformed_projects.json', 'r') as f:
        projects = json.load(f)

    for p in projects:
        cursor.execute("""
            MERGE Projects AS target
            USING (SELECT ? AS project_id) AS source
            ON target.project_id = source.project_id
            WHEN MATCHED THEN UPDATE SET
                project_name = ?, client = ?, domain = ?, location = ?,
                project_manager = ?, start_date = ?, end_date = ?, status = ?
            WHEN NOT MATCHED THEN
                INSERT (project_id, project_name, client, domain, location, project_manager, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, p["project_id"], p["project_name"], p["client"], p["domain"], p["location"],
             p["project_manager"], p["start_date"], p["end_date"], p["status"],
             p["project_id"], p["project_name"], p["client"], p["domain"], p["location"],
             p["project_manager"], p["start_date"], p["end_date"], p["status"])

    # Loading technologies
    with open('project_technologies.json', 'r') as f:
        techs = json.load(f)

    for t in techs:
        cursor.execute("""
            MERGE ProjectTechnologies AS target
            USING (SELECT ? AS project_id, ? AS technology) AS source
            ON target.project_id = source.project_id AND target.technology = source.technology
            WHEN NOT MATCHED THEN
                INSERT (project_id, technology) VALUES (?, ?);
        """, t["project_id"], t["technology"], t["project_id"], t["technology"])

    conn.commit()
    cursor.close()
    conn.close()

    print(f" Loaded {len(projects)} projects and {len(techs)} technologies into SQL Server")

if __name__ == "__main__":
    load()
