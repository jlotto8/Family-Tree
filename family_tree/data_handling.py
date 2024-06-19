# This module handles reading and validating data from a CSV file.
import csv
from person import Person

def read_data(filename):
    people = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = Person(
                id=int(row['ID']),
                name=row['Name'],
                gender=row['Gender'],
                birth=row.get('Birth Date'),
                death=row.get('Death Date')
            )
            people[person.id] = person
    return people

def validate_relationships(filename, people):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = people[int(row['ID'])]
            # Validate spouse
            if row['Spouse ID']:
                spouse_id = int(row['Spouse ID'])
                if spouse_id not in people:
                    raise ValueError(f"Spouse ID {spouse_id} does not exist.")
                person.spouse = people[spouse_id]
            # Validate children
            if row['Children IDs']:
                children_ids = [int(id) for id in row['Children IDs'].split(';') if id]
                for child_id in children_ids:
                    if child_id not in people:
                        raise ValueError(f"Child ID {child_id} does not exist.")
                person.children = [people[id] for id in children_ids]
