#include <iosstream>
using namespace std;

void displayMessage() {
    cout << "==== Assignment Optimizer ====" << endl;
    cout << "1. Generate Dataset" << endl;
    cout << "2. Run EDF" << endl;
    cout << "3. Run SJF" << endl;
    cout << "4. Results" << endl;
    cout << "5. Exit" << endl;
}

int main() {
    int choice;
    do {
        displayMessage();
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Generating dataset..." << endl;
                // Call dataset generation function here
                break;
            case 2:
                cout << "Running EDF algorithm..." << endl;
                // Call EDF algorithm function here
                break;
            case 3:
                cout << "Running SJF algorithm..." << endl;
                // Call SJF algorithm function here
                break;
            case 4:
                cout << "Displaying results..." << endl;
                system("python3 src/plot_results.py");
                break;
            case 5:
                cout << "Exiting program." << endl;
                break;
            default:
                cout << "Invalid choice. Please try again." << endl;
        }
    } while (choice != 5);
    return 0;
}
