# -MN-2-Software-Solutions-Repo-P1

To run the program for Project 1 (solving a single drone path):
1. You must first have the latest version of Python installed.
2. Open the Main Algorithm folder in terminal.
3. Run pip install -r requirements.txt
4. From the Main Algorithm folder, run python ./ComputeDronePath.py
5. Provide the file path for the algorithm to solve for.

Note: All 3 algorithm are present within the main python file. Change the variable 'algNum' to change which algorithm is used. 1 is the random search, 2 is for pruning, 3 is for nearest neighbor.

To run the program for Project 2 (solving with 1+ drones & clustering):
1. You must first have the latest version of Python installed.
2. Open the KNN_Algorithms_P2 folder in terminal.
3. Run pip install -r requirements.txt
4. From the Main Algorithm folder, run python ./ComputeLargeDronePath.py
5. Provide the file path for the algorithm to solve for.

To run the program for Project 3, you have 2 options:
1. py -3.13 -m pip install -r requirements.txt
2. pyinstaller main.spec
3. Checkout the dist folder it generates
4. Run main.exe
OR
1. Checkout A-Star_Algorithm_P3
2. Run py -3.13 -m venv kivyenv
3. Run ./kivyenv/Scripts/activate
4. py -3.13 -m pip install -r requirements.txt
5. Run python ./main.py