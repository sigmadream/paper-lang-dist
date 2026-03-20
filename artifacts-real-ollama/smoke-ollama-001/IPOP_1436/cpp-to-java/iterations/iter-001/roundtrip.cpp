#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    int count = 0;
    int value = 665;
    while (count < n) {
        ++value;
        if (to_string(value).find("666") != string::npos) {
            ++count;
        }
    }

    cout << value << endl;
    return 0;
}
