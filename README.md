-MN-2-Software-Solutions-Repo-P1

# Project 1: Single Drone Path

To run the program:

1. Make sure you have Python 3.13.9 installed.
2. Open the Main Algorithm folder in the terminal.
3. Install dependencies:
   pip install -r requirements.txt
4. Run the algorithm:
   python ./ComputeDronePath.py
5. Provide the file path when prompted.

Note:
All 3 algorithms are included in the main Python file. Change the variable algNum to select the algorithm:

- 1 – Random Search
- 2 – Pruning
- 3 – Nearest Neighbor

---

# Project 2: Multiple Drones & Clustering

To run the program:

1. Make sure you have Python 3.13.9 installed.
2. Open the KNN_Algorithms_P2 folder in the terminal.
3. Install dependencies:
   pip install -r requirements.txt
4. Run the algorithm:
   python ./ComputeLargeDronePath.py
5. Provide the file path when prompted.

---

# Project 3: A-Star Ship Balancing

To run the program, you have two options:

## Option 1: Using PyInstaller

1. Install dependencies:
   py -3.13 -m pip install -r requirements.txt
2. Build the executable using PyInstaller:
   pyinstaller main.spec
3. Go to the dist folder and run:
   main.exe

## Option 2: Using the Python Script Directly

1. Go to A-Star_Algorithm_P3.
2. Create a virtual environment:
   py -3.13 -m venv kivyenv
3. Activate the virtual environment:
   ./kivyenv/Scripts/activate
4. Install dependencies:
   py -3.13 -m pip install -r requirements.txt
5. Run the program:
   python ./main.py

---

Notes

- Make sure to always use the correct Python version for each project (py -3.13 for Project 3).
- Each project folder contains its own requirements.txt and Python scripts.
- Adjust algNum in Project 1 if you want to switch between algorithms.
- For Project 2, ensure your input files match the expected format for clustering/multi-drone paths.
