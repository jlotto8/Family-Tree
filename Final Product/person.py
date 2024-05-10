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