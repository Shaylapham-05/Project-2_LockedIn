#include <iosstream>
#include <fstream>
#include <sstream>
#include <vector>
#include <chrono>
#include "heap.h"
using namespace std;

vector<Task> tasks(const string& filename) {
    vector<Task> taskList;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return taskList;
    }
    string line;
    while (getline(file, line)) {
        istringstream iss(line);
        int id, arrival, duration, deadline;
        if (!(iss >> id >> arrival >> duration >> deadline)) { break; }
        taskList.push_back({id, arrival, duration, deadline});
    }
    file.close();
    return taskList;
}

