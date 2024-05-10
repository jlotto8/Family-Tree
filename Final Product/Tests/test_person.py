import unittest
from person import Person

class TestPerson(unittest.TestCase):
    def test_initialization(self):
        # Create a person with some hypothetical attributes
        person = Person(id=1, name="John Doe", gender="M", birth="1990-01-01", death="2070-01-01")

        # Test initialization of attributes
        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "John Doe")
        self.assertEqual(person.gender, "M")
        self.assertEqual(person.birth, "1990-01-01")
        self.assertEqual(person.death, "2070-01-01")
        self.assertIsNone(person.spouse)
        self.assertIsInstance(person.children, list)
        self.assertEqual(len(person.children), 0)

    def test_setting_spouse(self):
        # Create two person objects
        person1 = Person(id=1, name="John Doe", gender="M")
        person2 = Person(id=2, name="Jane Doe", gender="F")
        
        # Set person2 as the spouse of person1
        person1.spouse = person2

        # Test the spouse attribute
        self.assertIs(person1.spouse, person2)
        self.assertEqual(person1.spouse.name, "Jane Doe")

    def test_adding_children(self):
        # Create a person and children
        parent = Person(id=1, name="John Doe", gender="M")
        child1 = Person(id=2, name="Child One", gender="M")
        child2 = Person(id=3, name="Child Two", gender="F")
        
        # Simulate adding children
        parent.children.append(child1)
        parent.children.append(child2)

        # Test children attribute
        self.assertEqual(len(parent.children), 2)
        self.assertIs(parent.children[0], child1)
        self.assertIs(parent.children[1], child2)

if __name__ == '__main__':
    unittest.main()
