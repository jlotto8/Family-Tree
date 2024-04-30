# Family-Tree

This project generates a visual representation of a family tree using data provided in CSV files. It utilizes Python for data processing and Graphviz for visualizing the family tree in a hierarchical format.

## Features

- **Data Parsing**: Reads individual and relationship data from CSV files.
- **Object-Oriented Programming**: Utilizes a custom `Person` class to store individual and relationship data.
- **Graph Visualization**: Creates and saves a visual family tree using Graphviz, highlighting different relationships and attributes.

## Prerequisites

To run this project, you need:
- Python 3.x
- Pandas library
- Graphviz library

## Installation

You can install the necessary Python libraries using pip:
bash pip install pandas graphviz. Make sure Graphviz is also installed on your system. For Graphviz installation instructions, visit Graphviz's website 

## Project Files

- `Individuals.csv`: Contains data about individuals such as name, gender, birth and death dates.
- `Relationships.csv`: Contains data about relationships between individuals like parent-child and marital relationships.
- `family_tree.py`: Python script that reads the CSV files, creates Person objects, establishes relationships, and generates the family tree graph.

## Setup

1. Ensure all prerequisites are installed.
2. Clone this repository or download the files to your local machine.
3. Place the `Individuals.csv` and `Relationships.csv` in the same directory as the script.


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