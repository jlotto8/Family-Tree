from graphviz import Digraph
import csv 

class Person:
    def __init__(self, id, name, gender, birth=None, death=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.birth = birth
        self.death = death
        self.spouse = None
        self.children = []
        self.parent = None  

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

    # Validate Spouse IDs
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = people[int(row['ID'])]
            if row['Spouse ID']:
                spouse_id = int(row['Spouse ID'])
                if spouse_id not in people:
                    raise ValueError(f"Spouse ID {spouse_id} does not exist. Please review your input data.")
                person.spouse = people[spouse_id]

    # Validate Children IDs
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            person = people[int(row['ID'])]
            if row['Children IDs']:
                children_ids = [int(x) for x in row['Children IDs'].split(';') if x]
                for child_id in children_ids:
                    if child_id not in people:
                        raise ValueError(f"Child ID {child_id} does not exist. Please review your input data.")
                person.children = [people[child_id] for child_id in children_ids]

    return people


def create_family_tree(people):
    dot = Digraph('FamilyTree', format='png')
    dot.attr(rankdir='TB', splines='ortho')
    dot.attr('node', shape='ellipse', style='filled', fontname='Helvetica',width='1.9', height='1.8', margin='0.1', pad='2', fontsize='17')
    colors = {'M': 'lightblue3', 'F': 'plum1'}

    for person in people.values():
        birth_date = f"{person.birth}"
        dot.node(str(person.id), f"{person.name} \n {birth_date}", fillcolor=colors[person.gender], center='true')

    for person in people.values():
        if person.spouse and person.id < person.spouse.id:
            spouse_joint = f"joint_{person.id}_{person.spouse.id}"
            dot.node(spouse_joint, '', width='0.2', height='0.2', shape ='doublecircle', style='solid')

            # Connect spouses at the same rank
            with dot.subgraph() as s:
                s.attr(rank='same')
                s.edge(str(person.id), spouse_joint, style='bold', color='red', len='0.7', dir='none')
                s.edge(spouse_joint, str(person.spouse.id), style='bold', color='red', len='0.7', dir='none')

            # Connect to children with extended vertical edges
            if person.children:
                child_connect = f"child_connect_{person.id}"
                dot.node(child_connect, '', width='0.2', height='0.2', shape = 'star',) #style='invis'
                dot.edge(spouse_joint, child_connect, style='solid', len='2.0', weight='3', dir='none')
                for child in person.children:
                    dot.edge(child_connect, str(child.id), style='solid', len='2.0', weight='3', dir='none')
        elif person.children and person.spouse is None: # Check if the person has no spouse
            child_connect = f"child_connect_{person.id}"
            dot.node(child_connect, '', width='0.2', height='0.2', shape='star') # style='invis'
            dot.edge(str(person.id), child_connect, style='solid', len='2.0', weight='3', dir='none')
            for child in person.children:
                dot.edge(child_connect, str(child.id), style='solid', len='2.0', weight='3', dir='none')

    dot.render('output/family_tree', view=True)


def main():
    people = read_data('union2.csv')
    create_family_tree(people)

if __name__ == "__main__":
    main()