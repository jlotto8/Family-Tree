from graphviz import Digraph
from data_handling import read_data, validate_relationships

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

# This is the main script for creating the family tree using Graphviz.
def main():
    people = read_data('family_data.csv') # Read data from the CSV file and create Person objects
    validate_relationships('family_data.csv', people) # Validates input data from csv
    create_family_tree(people) # # Create a family tree graph using the created Person objects
    # Output the graph...

# # Check if the script is being run directly
if __name__ == "__main__":
    main()  # Call the main function to start the program