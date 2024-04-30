"""
This prgram is designed to create a family tree using data stored in two CSV files: one containing individual details and the other containing relationships between these individuals. It uses the Graphviz tool to visualize the family tree.
"""
import pandas as pd
import graphviz

# Represents a single indvidual in the famliy tree. All attributes except id, name, and gender are optional (not all data will be known, or available ex death date if person is still living)
class Person:
    def __init__(self, id, name, gender, birth_date=None, death_date=None, birth_location=None, other_details=None):
        self.id = id
        self.name = name
        self.gender = gender.strip()  # Ensure no extra spaces
        self.birth_date = birth_date
        self.death_date = death_date
        self.birth_location = birth_location
        self.other_details = other_details
        self.spouse = []
        self.children = []
        self.parents = []
        self.siblings = []

# Reads individuals from a CSV file and creates a Person object for each.
# Process: Opens the CSV file and reads each row. For each row, it creates a Person object, filling in all the details from the CSV. Adds each Person object to a dictionary with their id as the key.
def read_individuals(filename):
    df = pd.read_csv(filename)
    people = {}
    for index, row in df.iterrows(): # pandas dataframe 
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
    return people

def read_relationships(filename, people):
    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        person1_id = int(row['Person1_ID'])
        person1 = people[person1_id]
        person2_ids = row['Person2_IDs'].split(';')

        for person2_id in person2_ids:
            person2_id = int(person2_id.strip())  # Trim any spaces
            person2 = people[person2_id]
            if row['Relationship'] == 'Spouse':
                person1.spouse.append(person2)
                person2.spouse.append(person1)
            elif row['Relationship'] in ['Mother', 'Father']:
                person1.children.append(person2)
                person2.parents.append(person1)
            elif row['Relationship'] == 'Sibling':
                person1.siblings.append(person2)
                person2.siblings.append(person1)

def create_family_tree_graph(people):
    dot = graphviz.Digraph('Family Tree', format='png')
    dot.attr(rankdir='TB', size='10,10')

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

    for person in people.values():
        for child in person.children:
            dot.edge(str(person.id), str(child.id), label='Parent', color='blue')
        for spouse in person.spouse:
            if person.id < spouse.id:
                dot.edge(str(person.id), str(spouse.id), label='Spouse', dir='none', color='red')
        for sibling in person.siblings:
            if person.id < sibling.id:
                dot.edge(str(person.id), str(sibling.id), label='Sibling', dir='none', color='green')

    output_path = 'output/family_tree'
    dot.render(output_path, view=True)
    print(f"Graph rendered and saved to {output_path}.gv and {output_path}.png")

def main():
    people = read_individuals('Individuals.csv')
    read_relationships('relationships.csv', people)
    create_family_tree_graph(people)

if __name__ == "__main__":
    main()
