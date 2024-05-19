import unittest
from unittest.mock import patch, MagicMock
from person import Person
from family_tree import create_family_tree

class TestFamilyTree(unittest.TestCase):
    def setUp(self):
        self.people = {
            1: Person(1, "John Doe", "M", "1990"),
            2: Person(2, "Jane Smith", "F", "1989"),
            3: Person(3, "Child One", "M", "2010")
        }
        self.people[1].spouse = self.people[2]
        self.people[1].children.append(self.people[3])
        self.people[2].children.append(self.people[3])

@patch('family_tree.Digraph')
def test_create_family_tree(self, mock_digraph):
    # Call the function under test
    create_family_tree(self.people)

    # Retrieve the mock instance of Digraph
    dot = mock_digraph.return_value

    # Counting nodes and edges
    personal_nodes = len(self.people)
    relationship_nodes = sum(1 for person in self.people.values() if person.spouse)  # one for each spouse pair
    special_nodes = sum(1 for person in self.people.values() if person.children)  # one for each parent with children
    total_expected_nodes = personal_nodes + relationship_nodes + special_nodes
    self.assertEqual(dot.node.call_count, total_expected_nodes)

    # Each spouse relationship adds 2 edges, each parent-child relationship adds at least one, plus one for each child
    spouse_edges = 2 * relationship_nodes
    child_edges = sum(2 + len(person.children) for person in self.people.values() if person.children)
    total_expected_edges = spouse_edges + child_edges
    self.assertEqual(dot.edge.call_count, total_expected_edges)


if __name__ == '__main__':
    unittest.main()






