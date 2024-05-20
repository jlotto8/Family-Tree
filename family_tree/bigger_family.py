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

import csv
from graphviz import Digraph

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

    add_legend(dot)
    dot.render('output/bigger_tree', view=True)  # Render the family tree graph as a PNG image


def add_legend(dot):
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', color='black',style='bold', fontsize='24')  
        legend.node('Male', 'Male', fillcolor='lightblue3', shape='ellipse', width='1', height='0.5', fixedsize='true')  
        legend.node('Female', 'Female', fillcolor='plum1', shape='ellipse', width='1', height='0.5', fixedsize='true')  
        legend.node('SpouseJoint', '', shape='doublecircle', style='solid', width='0.4', height='0.4')  
        legend.node('ChildConnect', '', shape='star', style='solid', width='0.4', height='0.4')  
        legend.edge('SpouseJoint', 'ChildConnect', label='Parent to Child Connection', style='solid', dir='none', fontsize='21')
        legend.edge('Male', 'SpouseJoint', label='Spouse Connection', style='bold', color='red', dir='none', fontsize='21')
   

# This is the main script for creating the family tree using Graphviz.
def main():
    people = read_data('bigger.csv') # Read data from the CSV file and create Person objects
    validate_relationships('bigger.csv', people) # Validates input data from csv
    create_family_tree(people) # # Create a family tree graph using the created Person objects
    # Output the graph...

# # Check if the script is being run directly
if __name__ == "__main__":
    main()  # Call the main function to start the program

