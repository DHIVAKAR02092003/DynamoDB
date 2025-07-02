import pandas as pd 

def transform(data):

    project_info = data[['project_id', 'project_name']] #to call a project_id with project_name
    columns = data.columns.tolist()  #list the column names
    df1 = data[['project_id', 'project_name', 'client', 'domain', 'location','project_manager', 'start_date'
                  ,'end_date', 'status']]
    mapped = []
    
    for _ ,row in data.iterrows():
        pid = row['project_id']
        tech_list = row['technologies']
        for tech in tech_list:
            mapped.append({'Project_id': pid, 'technology': tech.strip()})

    df2 = pd.DataFrame(mapped)
    
    return df1, df2
    