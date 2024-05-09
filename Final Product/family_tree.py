# Import necessary libraries
from graphviz import Digraph  # Import Digraph class from graphviz for drawing family tree graphs
import csv  # Import CSV module for reading CSV files

# Define a class for representing a person
class Person:
    def __init__(self, id, name, gender, birth=None, death=None):
        # Initialize attributes of the Person class
        self.id = id  # Unique identifier for each person
        self.name = name  # Name of the person
        self.gender = gender  # Gender of the person ('M' for male, 'F' for female)
        self.birth = birth  # Birth date of the person
        self.death = death  # Death date of the person (if applicable)
        self.spouse = None  # Reference to the spouse of the person
        self.children = []  # List of references to the children of the person
        self.parent = None  # Reference to the parent of the person (not used in this code)

# Function to read data from a CSV file and create Person objects
def read_data(filename):
    people = {}  # Dictionary to store Person objects with their IDs as keys
    # Open the CSV file using a context manager
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Create a CSV reader object
        # Iterate over each row in the CSV file
        for row in reader:
            # Create a Person object with data from the CSV row
            person = Person(
                id=int(row['ID']),
                name=row['Name'],
                gender=row['Gender'],
                birth=row.get('Birth Date'),
                death=row.get('Death Date')
            )
            people[person.id] = person  # Add the Person object to the dictionary using its ID as the key

    # Validate Spouse IDs
    # Reopen the CSV file to validate spouse IDs after creating all Person objects
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Create another CSV reader object
        # Iterate over each row in the CSV file again
        for row in reader:
            person = people[int(row['ID'])]  # Get the Person object corresponding to the current row's ID
            if row['Spouse ID']:
                spouse_id = int(row['Spouse ID'])  # Get the spouse ID from the CSV row
                if spouse_id not in people:  # Check if the spouse ID exists in the dictionary
                    raise ValueError(f"Spouse ID {spouse_id} does not exist. Please review your input data.")
                person.spouse = people[spouse_id]  # Set the spouse attribute of the Person object

    # Validate Children IDs
    # Reopen the CSV file to validate children IDs after creating all Person objects
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Create another CSV reader object
        # Iterate over each row in the CSV file again
        for row in reader:
            person = people[int(row['ID'])]  # Get the Person object corresponding to the current row's ID
            if row['Children IDs']:
                children_ids = row['Children IDs'].split(';')  # Split children IDs separated by ';'
                valid_children_ids = []  # List to store valid child IDs
                for child_id_str in children_ids:
                    if child_id_str:
                        child_id = int(child_id_str)  # Convert child ID from string to integer
                        if child_id not in people:  # Check if the child ID exists in the dictionary
                            raise ValueError(f"Child ID {child_id} does not exist. Please review your input data.")
                        valid_children_ids.append(child_id)  # Add valid child IDs to the list
                person.children = [people[child_id] for child_id in valid_children_ids]  # Set children attribute

    return people  # Return the dictionary of Person objects

# Function to create a family tree graph using Graphviz
def create_family_tree(people):
    dot = Digraph('FamilyTree', format='png')  # Create a Digraph object for the family tree
    dot.attr(rankdir='TB', splines='ortho')  # Set graph attributes (orientation and edge style)
    dot.attr('node', shape='ellipse', style='filled', fontname='Helvetica', width='2.7', height='1.8', margin='0.1', pad='2', fontsize='18')  # Set node attributes
    colors = {'M': 'lightblue3', 'F': 'plum1'}  # Define colors for male and female nodes

    # Add nodes for each Person object to the graph
    for person in people.values():
        birth_date = f"{person.birth}"  # Get the birth date of the person
        dot.node(str(person.id), f"{person.name} \n {birth_date}", fillcolor=colors[person.gender], center='true')  # Add node with name and birth date

    # Connect nodes to represent family relationships
    for person in people.values():
        if person.spouse and person.id < person.spouse.id:
            spouse_joint = f"joint_{person.id}_{person.spouse.id}"  # Create a unique ID for the joint node of spouses
            dot.node(spouse_joint, '', width='0.2', height='0.2', shape='doublecircle', style='solid')  # Add joint node for spouses

            # Connect spouses at the same rank
            with dot.subgraph() as s:
                s.attr(rank='same')  # Set rank attribute for the subgraph
                s.edge(str(person.id), spouse_joint, style='bold', color='red', len='0.7', dir='none')  # Connect person to spouse joint node
                s.edge(spouse_joint, str(person.spouse.id), style='bold', color='red', len='0.7', dir='none')  # Connect spouse joint node to spouse

            # Connect to children with extended vertical edges
            if person.children:  # Check if the person has children
                child_connect = f"child_connect_{person.id}"  # Create a unique ID for child connection
                dot.node(child_connect, '', width='0.2', height='0.2', shape='star')  # Add node for child connection
                dot.edge(spouse_joint, child_connect, style='solid', len='2.0', weight='3', dir='none')  # Connect spouse joint to child connection node
                for child in person.children:
                    dot.edge(child_connect, str(child.id), style='solid', len='2.0', weight='3', dir='none')  # Connect child connection node to children nodes
        elif person.children and person.spouse is None:  # Check if the person has no spouse but has children
            child_connect = f"child_connect_{person.id}"  # Create a unique ID for child connection
            dot.node(child_connect, '', width='0.2', height='0.2', shape='star')  # Add node for child connection
            dot.edge(str(person.id), child_connect, style='solid', len='2.0', weight='3', dir='none')  # Connect person to child connection node
            for child in person.children:
                dot.edge(child_connect, str(child.id), style='solid', len='2.0', weight='3', dir='none')  # Connect child connection node to children nodes

    dot.render('output/family_tree', view=True)  # Render the family tree graph as a PNG image

# Main function to execute the program
def main():
    people = read_data('union2.csv')  # Read data from the CSV file and create Person objects
    create_family_tree(people)  # Create a family tree graph using the created Person objects

# Check if the script is being run directly
if __name__ == "__main__":
    main()  # Call the main function to start the program
