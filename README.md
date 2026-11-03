# Self-Balancing Binary Search Tree – Implementation and Comparison

## Project Overview

This project implements and compares three tree data structures:

- **Binary Search Tree (BST)**
- **AVL Tree**
- **Red-Black Tree**

The project is based on the MediQueue telemedicine scenario. Patient records are identified by numeric Patient IDs. The aim is to study how different tree structures handle insertion, searching and deletion, especially when IDs are entered in sequential order.

A normal BST can become unbalanced when values are inserted in sorted order. AVL and Red-Black Trees use self-balancing techniques to keep their height under control and maintain efficient operations.

## Repository Contents

| File | Description |
|---|---|
| `LAB5_DSA_528.py` | Main Python program containing the tree implementations and comparison experiments |
| `comparison_results_3_trees.csv` | CSV file containing the recorded experimental results |
| `three_tree_height_comparison.png` | Graph comparing the heights of the three trees |

## Technologies Used

- Python 3
- Matplotlib
- Python standard-library modules: `random`, `time`, `math` and `csv`

## Data Structures

### 1. Binary Search Tree (BST)

A BST stores smaller keys in the left subtree and larger keys in the right subtree.

Operations include:
- Insertion
- Searching
- Deletion
- Inorder traversal
- Height calculation

The BST does not automatically balance itself. Its worst-case time complexity for searching, insertion and deletion is **O(n)**.

### 2. AVL Tree

An AVL Tree is a self-balancing BST. It maintains a balance factor of -1, 0 or +1 at every node.

It uses four rotation cases:
- Left-Left (LL)
- Right-Right (RR)
- Left-Right (LR)
- Right-Left (RL)

Searching, insertion and deletion take **O(log n)** time in the worst case.

### 3. Red-Black Tree

A Red-Black Tree is a self-balancing BST in which every node is assigned either Red or Black colour.

It maintains balance using:
- Recolouring
- Left rotation
- Right rotation

Searching, insertion and deletion take **O(log n)** time in the worst case.

## Experimental Setup

The program compares the trees using three input patterns:

| Dataset | Description |
|---|---|
| Sequential | Patient IDs inserted in ascending order |
| Random | Patient IDs inserted in random order |
| Nearly sorted | Ascending IDs with approximately 5% of positions swapped |

The experiment uses input sizes of:

- 1,000 elements
- 5,000 elements
- 10,000 elements

A fixed random seed is used for reproducible workload generation.

## Performance Measurements

The program records and compares:
- Tree height after insertion
- Theoretical minimum-height reference
- Total insertion time
- Number of rotations
- Average comparisons per successful search
- Tree height after deleting 20% of the keys

## Sample Observation

For sequential insertion of 10,000 elements, the recorded tree heights were:

| Tree | Height |
|---|---:|
| BST | 10,000 |
| AVL Tree | 14 |
| Red-Black Tree | 24 |

This observation shows that a normal BST can become highly skewed when values are inserted in ascending order. AVL and Red-Black Trees maintain much smaller heights through balancing.

*The exact execution times and results may vary depending on the computer and execution environment.*

## Requirements

- Python 3.10 or later
- Matplotlib

Install Matplotlib using:

```bash
python -m pip install matplotlib
```

The `random`, `time`, `math` and `csv` modules are included with Python and do not need separate installation.

## How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/ANAY808-GIT/YOUR-REPOSITORY-NAME.git
```

Replace `YOUR-REPOSITORY-NAME` with the actual repository name shown on GitHub.

### Step 2: Open the project folder

```bash
cd YOUR-REPOSITORY-NAME
```

### Step 3: Install the required library

```bash
python -m pip install matplotlib
```

### Step 4: Run the Python program

```bash
python LAB5_DSA_528.py
```

On Windows, if the `python` command is not recognized, try:

```bash
py LAB5_DSA_528.py
```

The program will display the experiment results in the terminal. The CSV and graph files shown in this repository contain the saved comparison outputs from the experiment.

## Conclusion

This project demonstrates why self-balancing trees are useful when data arrives in sorted or nearly sorted order. A normal BST is simple but can become inefficient when it is highly skewed. AVL Trees maintain strict height balance, while Red-Black Trees use colour-based rules for more flexible balancing. Both self-balancing structures provide logarithmic worst-case time complexity for their main operations.

## Academic Details

- **Programme:** MSc Artificial Intelligence & Machine Learning
- **Course:** Data Structures and Algorithms Laboratory
- **Lab Topic:** Self-Balancing Binary Search Tree – Implementation and Comparison
- **Scenario:** MediQueue patient-record indexing
- **Programming Language:** Python
