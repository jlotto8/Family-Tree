# Family Tree Visualization

This project generates a visual representation of a family tree using data provided in CSV files. It utilizes Python for data processing and Graphviz for visualizing the family tree in a hierarchical format.
It represent that data from the csv as objects in Python, and then visualize the relationships between those objects using a graph. The relationships include spouses, children, and potentially other types of relationships like siblings or cousins.

## Features

- **Data Parsing**: Reads individual and relationship data from CSV files.
- **Object-Oriented Programming**: Utilizes a custom `Person` class to store individual and relationship data.
- **Graph Visualization**: Creates and saves a visual family tree using Graphviz, highlighting different relationships and attributes.

## Prerequisites

To run this project, you need:
- Python 3.x
- Graphviz library

## Installation

You can install the necessary Python libraries using pip:
bash pip install graphviz. Make sure Graphviz is also installed on your system. 
For Graphviz installation instructions, visit Graphviz's website 

# Importing Libraries
The project begins by importing necessary libraries:

from graphviz import Digraph
import csv 

- Digraph from graphviz is used to create directed graphs, ideal for representing relationships like parent-child or spouse-spouse.
- The csv module is used for reading data from CSV files.


## Project Files

- `family_data.csv`: Contains data about individuals such as name, gender, birth and death dates. Contains data about relationships between individuals like parent-child and spousal/union relationships.
- `data_handling.py`:  Python script that reads the CSV files, creates Person objects, establishes relationships, and  validates input data
- `family_tree.py`: Generates the family tree graph.

## Setup

1. Ensure all prerequisites are installed.
2. Clone this repository or download the files to your local machine.
3. Place the 'family_data.csv` in the same directory as the script.


## Running the Script

Navigate to the directory containing the script and run the following command in your terminal:

bash

python family_tree.py

The script will read the data, process it, and generate a PNG image of the family tree which will be saved in the output directory. It will also generate a Graphviz DOT file for further customization or debugging.

##  Output

The family tree is saved as family_tree.png in the output directory.
A DOT file family_tree.gv is also saved, which can be edited to manually adjust the graph if needed.

## Contributing

Feel free to fork this project and submit pull requests. You can also open an issue if you find bugs or have feature requests.
