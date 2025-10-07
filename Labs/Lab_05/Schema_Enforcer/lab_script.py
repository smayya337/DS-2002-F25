import csv
import json
import pandas as pd

def create_csv_data():
    data = [
        ['student_id', 'major', 'GPA', 'is_cs_major', 'credits_taken'],
        [1001, 'Computer Science', 3.8, 'Yes', '120.5'],
        [1002, 'Computer Science', 3, 'Yes', '105.0'],
        [1003, 'Mathematics', 3.5, 'No', '90'],
        [1004, 'Economics', 4, 'No', '115.5'],
        [1005, 'Statistics', 3.9, 'Yes', '110.0']
    ]
    with open('raw_survey_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def create_json_data():
    course_catalog = [
        {
            "course_id": "DS2002",
            "section": "001",
            "title": "Data Science Systems",
            "level": 2000,
            "instructors": [
                {"name": "Austin Rivera", "role": "Primary"},
                {"name": "Heywood Williams-Tracy", "role": "TA"}
            ]
        },
        {
            "course_id": "CS4260",
            "section": "001",
            "title": "Internet Scale Applications",
            "level": 4000,
            "instructors": [
                {"name": "Derrick Stone", "role": "Primary"}
            ]
        },
        {
            "course_id": "STS4500",
            "section": "001",
            "title": "STS and Engineering Practice",
            "level": 4000,
            "instructors": [
                {"name": "Caitlin Wylie", "role": "Primary"}
            ]
        },
        {
            "course_id": "EBUS4810",
            "section": "001",
            "title": "New Product Development",
            "level": 4000,
            "instructors": [
                {"name": "Adarsh Ramakrishnan", "role": "Primary"}
            ]
        }
    ]
    with open('raw_course_catalog.json', 'w') as jsonfile:
        json.dump(course_catalog, jsonfile, indent=2)

def clean_csv_data():
    df = pd.read_csv('raw_survey_data.csv')
    df['is_cs_major'] = df['is_cs_major'].replace({'Yes': True, 'No': False})
    df = df.astype({
        'credits_taken': 'float64',
        'GPA': 'float64'
    })
    df.to_csv('clean_survey_data.csv', index=False)

def normalize_json_data():
    with open('raw_course_catalog.json', 'r') as jsonfile:
        course_data = json.load(jsonfile)
    df_normalized = pd.json_normalize(
        course_data,
        record_path=['instructors'],
        meta=['course_id', 'section', 'title', 'level'],
        errors='ignore'
    )
    df_normalized.to_csv('clean_course_catalog.csv', index=False)

if __name__ == "__main__":
    # create_csv_data()
    # create_json_data()
    # clean_csv_data()
    normalize_json_data()