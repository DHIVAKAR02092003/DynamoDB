import json

def transform():
    with open('raw_data.json', 'r') as f:
        data = json.load(f)          #read the data

    projects = []
    technologies = []

    for project in data:
        projects.append({
            "project_id": project["project_id"],
            "project_name": project["project_name"],
            "client": project["client"],
            "domain": project["domain"],
            "location": project["location"],
            "project_manager": project["project_manager"],
            "start_date": project["start_date"],
            "end_date": project["end_date"],
            "status": project["status"]
        })

        for tech in project.get("technologies", []):
            technologies.append({
                "project_id": project["project_id"],
                "technology": tech
            })

    with open('transformed_projects.json', 'w') as f:
        json.dump(projects, f, indent=2)

    with open('project_technologies.json', 'w') as f:
        json.dump(technologies, f, indent=2)

    print(f"Transformed: {len(projects)} projects and {len(technologies)} technologies")

if __name__ == "__main__":
    transform()