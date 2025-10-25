#include <algorithm>
#include <iostream>
#include <conio.h>
#include <fstream>
#include <random>
#include <vector>
#include <limits>
#include <string>
#include <cmath>

using namespace std;

//class for Node objects
class Node {
private:
    int num;
    double x;
    double y;
public:
    Node(int newNum, double newX, double newY) : num(newNum), x(newX), y(newY){};
    int getNum(){
        return num;
    }
    double getX(){
        return x;
    }
    double getY(){
        return y;
    }
};

//calculates distance between two Nodes
double distance(Node& a, Node& b) {
    return sqrt(pow((b.getX() - a.getX()),2)+pow((b.getY() - a.getY()),2));
}

//calculates total path distance of current Node organization
double totalDistance(vector<Node>& currPath) {
    double result = 0;
    for (int i = 0; i < currPath.size() - 1; ++i){
        result += distance(currPath[i], currPath[i+1]);
    }
    result += distance(currPath.back(), currPath.front());
    return result;
}

//randomly shuffles order, replacing shortestDistance if new shortest is generated (outputs final shortest in place of eventual .txt output with all information)
int randomSearchUntilEnter(vector<Node>& Path, vector<Node>& shortestPath){
    double shortestDistance = INFINITY;
    shortestPath = Path;
    random_device rd;
    default_random_engine rng(rd());
    while(1){
        //checks if user inputs 'Enter' (AKA carriage return or '\r' for getch)
        if (_kbhit()){
            char input = _getch();
            if (input == '\r'){
                break;
            }
        }
        //randomly shuffles inner nodes (leaving start and end same), generates current distance and shortens to one decimal place
        shuffle(Path.begin() + 1, Path.end() - 1, rng);
        double currDistance = totalDistance(Path);
        currDistance = currDistance - fmod(currDistance, 0.1);
        //saves current shortest distance as well as node visit order (current path)
        if (currDistance < shortestDistance){
            shortestDistance = currDistance;
            shortestPath = Path;
            cout << "       " << shortestDistance << endl;
        }
    }
    //return shortest distance as a whole number (no decimals, so use 'ceil' AKA ceiling)
    return ceil(shortestDistance);
}

//find nearest neighbor of first node, then nearest neighbor of that node not including visited node, repeat...
//(try to change it up occasionally, going to the second or third closest neighbor instead to vary results)
double nearestNeighborSearchUntilEnter(vector<Node>& Path, vector<Node>& shortestPath){
    double shortestDistance = INFINITY;
    shortestPath = Path;
    vector<Node> notVisited = Path;
    //
}

int main() {
    //variable declarations
    string fileName;
    ifstream inputFile;
    ofstream outputFile;
    vector<Node> Path;
    vector<Node> shortestPath;

    //get file name, open file, check if bad, take in all coords, count
    cout << "Enter the name of file: ";
    cin >> fileName;
    inputFile.open(fileName);
    if (!inputFile.is_open()){
        cerr << "Error opening input file" << endl;
        return 1;
    }
    double A, B;
    int currPos = 1;
    while (inputFile >> A >> B){
        Path.push_back(Node(currPos, A, B));
        currPos++;
    }
    Node startAndEnd(Path[0]);
    Path.push_back(startAndEnd);
    inputFile.close();

    // cout << "First Path Order: ";
    // for (int j = 0; j < Path.size(); ++j){
    //     if (j < Path.size() - 1){
    //         cout << Path[j].getNum() << ", ";
    //     }
    //     else{
    //         cout << Path[j].getNum();
    //     }
    // }

    //begin outputting shortest paths
    cout << "There are " << Path.size() << " nodes, computing shortest route.." << endl;
    cout << "   Shortest Route Discovered So Far " << endl;

    //function runs until 'Enter' pressed, outputting 
    int resultDistance = randomSearchUntilEnter(Path, shortestPath);

    string fileOut = "";
    fileOut = fileName.substr(8, (fileName.size() - 4)) + "_SOLUTION_" + to_string(resultDistance) + ".txt";

    outputFile.open(fileOut);
    if (!outputFile.is_open()){
        cerr << "Error opening/creating output file" << endl;
        return 2;
    }

    cout << "Route written to disk as " << fileOut << endl;
    for (int j = 0; j < shortestPath.size(); ++j){
        if (j < shortestPath.size() - 1){
            outputFile << shortestPath[j].getNum() << ' ';
        }
        else{
            outputFile << shortestPath[j].getNum();
        }
    }

    outputFile.close();

    // cout << endl << "==========Results==========" << endl;
    // cout << "Shortest Path Distance: " << resultDistance << endl;
    // cout << "Shortest Path Order: ";
    // for (int j = 0; j < shortestPath.size(); ++j){
    //     if (j < shortestPath.size() - 1){
    //         cout << shortestPath[j].getNum() << ", ";
    //     }
    //     else{
    //         cout << shortestPath[j].getNum();
    //     }
    // }
    // cout << endl << "Shortest Path Image: *Image here*";

    return 0;
}