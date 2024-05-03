import pandas as pd
import graphviz

class Person:
    # Person class to hold individual family member information
    def __init__(self, id, name, gender, birth_date=None, death_date=None, birth_location=None, other_details=None):
        self.id = id  # Unique identifier for the person
        self.name = name  # Name of the person
        self.gender = gender.strip()  # Gender of the person, extra spaces removed
        self.birth_date = birth_date  # Optional: Birth date of the person
        self.death_date = death_date  # Optional: Death date of the person
        self.birth_location = birth_location  # Optional: Birth location of the person
        self.other_details = other_details  # Optional: Other details about the person
        self.spouse = None  # Spouse of the person
        self.children = []  # List of children (Person objects)
        self.parents = []  # List of parents (Person objects)

def read_data(filename):
    # Read CSV data and initialize Person instances
    df = pd.read_csv(filename)  # Read data from a CSV file into a DataFrame
    people = {}  # Dictionary to store Person instances, keyed by ID

    # Initialize each person from the row data
    for index, row in df.iterrows():
        person = Person(
            int(row['ID']),
            row['Name'],
            row['Gender'],
            row.get('Birth Date'),
            row.get('Death Date'),
            row.get('Birth Location'),
            row.get('Other Details')
        )
        people[int(row['ID'])] = person

    # Assign relationships after all Person instances have been created
    for index, row in df.iterrows():
        person = people[int(row['ID'])]

        # Assign spouse if exists
        if pd.notna(row['Spouse_ID']):
            spouse_id = int(row['Spouse_ID'])
            if spouse_id in people:
                person.spouse = people[spouse_id]
                people[spouse_id].spouse = person

        # Assign children if exist
        if pd.notna(row['Children IDs']):
            child_ids = row['Children IDs'].split(';')
            for child_id in child_ids:
                child_id = int(child_id.strip())
                person.children.append(people[child_id])
                people[child_id].parents.append(person)

    return people

# def create_family_tree_graph(people):
#     # Create the Graphviz graph
#     dot = graphviz.Digraph('Family Tree', format='png')
#     dot.attr(rankdir='TB', size='10,10', newrank='true')  # Set attributes for the graph

#     dot.attr('node', fontname='Helvetica', fontcolor='black', fontsize='24')
#     dot.attr('edge', fontname='Courier', fontcolor='black', fontsize='18')

#     # Define nodes and relationships for each person
#     for person in people.values():
#         node_shape = 'square' if person.gender == 'M' else 'ellipse'  # Choose shape based on gender
#         node_color = 'lightblue' if person.gender == 'M' else 'pink'  # Choose color based on gender

#         # Create a label for the node using HTML-like labels
#         # Adjust the font size for the name to be larger than the dates
#         node_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3"><TR><TD><FONT POINT-SIZE="19">{person.name}</FONT></TD></TR>'
#         if pd.notna(person.birth_date):  # Check if birth date is not null or NaN
#             # Make the birth date font size smaller
#             node_label += f'<TR><TD><FONT POINT-SIZE="15">Born: {int(person.birth_date)}</FONT></TD></TR>'  # Smaller font for birth date
#         if pd.notna(person.death_date):  # Check if death date is not null or NaN
#             # Make the death date font size smaller
#             node_label += f'<TR><TD><FONT POINT-SIZE="15">Died: {int(person.death_date)}</FONT></TD></TR>'  # Smaller font for death date
#         node_label += '</TABLE>>'

#         # Create node for each person with custom attributes
#         dot.node(str(person.id), label=node_label, shape=node_shape, style='filled', fillcolor=node_color)

#         # Create edges for parental relationships
#         for child in person.children:
#             dot.edge(str(person.id), str(child.id), label='Parent', color='blue')

#         # Create edges for spousal relationships
#         if person.spouse:
#             dot.edge(str(person.id), str(person.spouse.id), label='Spouse', dir='none', color='red')

#     output_path = 'output/family_tree'
#     dot.render(output_path, view=True)  # Render and save the graph
#     print(f"Graph rendered and saved to {output_path}.gv and {output_path}.png")

def create_family_tree_graph(people):
    # Create the Graphviz graph
    dot = graphviz.Digraph('Family Tree', format='png')
    dot.attr(rankdir='TB', size='10,10', newrank='true', bgcolor='lightgray')  # Set attributes for the graph

    # Define nodes and relationships for each person
    for person in people.values():
        node_shape = 'square' if person.gender == 'M' else 'ellipse'  # Choose shape based on gender
        node_color = 'lightblue' if person.gender == 'M' else 'pink'  # Choose color based on gender

        # Create a label for the node using HTML-like labels
        node_label = f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3"><TR><TD><FONT POINT-SIZE="19">{person.name}</FONT></TD></TR>'
        if pd.notna(person.birth_date):  # Check if birth date is not null or NaN
            node_label += f'<TR><TD><FONT POINT-SIZE="15">Born: {int(person.birth_date)}</FONT></TD></TR>'
        if pd.notna(person.death_date):  # Check if death date is not null or NaN
            node_label += f'<TR><TD><FONT POINT-SIZE="15">Died: {int(person.death_date)}</FONT></TD></TR>'
        node_label += '</TABLE>>'

        # Create node for each person with custom attributes
        dot.node(str(person.id), label=node_label, shape=node_shape, style='filled', fillcolor=node_color, width="1.5", height="0.5")

        # Create edges for parental relationships
        for child in person.children:
            dot.edge(str(person.id), str(child.id), label='Parent', color='blue')

        # Handle spousal relationships with rank=same to keep them on the same level
        if person.spouse and int(person.id) < int(person.spouse.id):  # To avoid duplicate edges
            # This subgraph ensures that spouses appear on the same horizontal level
            with dot.subgraph() as s:
                s.attr(rank='same')
                s.edge(str(person.id), str(person.spouse.id), label='Spouse', dir='none', color='red')

    output_path = 'output/family_tree'
    dot.render(output_path, view=True)  # Render and save the graph
    print(f"Graph rendered and saved to {output_path}.gv and {output_path}.png")


def main():
    # Main function to execute the program
    people = read_data('family_data.csv')  # Read data and process relationships
    create_family_tree_graph(people)  # Create and render the family tree graph

if __name__ == "__main__":
    main()
