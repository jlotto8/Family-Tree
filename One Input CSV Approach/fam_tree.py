import pandas as pd
import graphviz

class Person:
    def __init__(self, id, name, gender, birth_date=None, death_date=None, birth_location=None, other_details=None):
        self.id = id
        self.name = name
        self.gender = gender.strip()  # Ensure no extra spaces
        self.birth_date = birth_date
        self.death_date = death_date
        self.birth_location = birth_location
        self.other_details = other_details
        self.spouse = None
        self.children = []
        self.parents = []
        self.siblings = []

def read_data(filename):
    df = pd.read_csv(filename)
    people = {}

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

    # Assign relationships
    for index, row in df.iterrows():
        person = people[int(row['ID'])]

        # Process Spouse
        if pd.notna(row['Spouse_ID']):
            spouse_id = int(row['Spouse_ID'])
            person.spouse = people[spouse_id]

        # Process Children
        if pd.notna(row['Child_IDs']):
            child_ids = row['Child_IDs'].split(';')
            for child_id in child_ids:
                child_id = int(child_id.strip())
                person.children.append(people[child_id])
                people[child_id].parents.append(person)

        # Process Siblings
        if pd.notna(row['Sibling_IDs']):
            sibling_ids = row['Sibling_IDs'].split(';')
            for sibling_id in sibling_ids:
                sibling_id = int(sibling_id.strip())
                person.siblings.append(people[sibling_id])
                people[sibling_id].siblings.append(person)

    return people

def create_family_tree_graph(people):
    dot = graphviz.Digraph('Family Tree', format='png')
    dot.attr(rankdir='TB', size='10,10')

    # Add nodes and relationships to the graph
    for person in people.values():
        if person.gender == 'M':
            node_color = 'lightblue'
            node_shape = 'square'
        else:
            node_color = 'pink'
            node_shape = 'ellipse'

        node_label = f'{person.name}\n({person.gender})'
        if person.birth_date:
            node_label += f'\nBorn: {person.birth_date}'
        dot.node(str(person.id), label=node_label, style='filled', fillcolor=node_color, shape=node_shape)

        for child in person.children:
            dot.edge(str(person.id), str(child.id), label='Parent', color='blue')
        if person.spouse:
            dot.edge(str(person.id), str(person.spouse.id), label='Spouse', dir='none', color='red')
        for sibling in person.siblings:
            if person.id < sibling.id:
                dot.edge(str(person.id), str(sibling.id), label='Sibling', dir='none', color='green')

    output_path = 'output/family_tree'
    dot.render(output_path, view=True)
    print(f"Graph rendered and saved to {output_path}.gv and {output_path}.png")

def main():
    people = read_data('combined_individuals_relationships.csv')
    create_family_tree_graph(people)

if __name__ == "__main__":  
    main()
