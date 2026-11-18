#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    // Parse T from the first line, ignoring leading/trailing whitespace.
    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    string numStr = line.substr(start, end - start + 1);
    int T = stoi(numStr);

    for (int i = 0; i < T; ++i) {
        if (!getline(cin, line)) break;

        // Remove possible carriage return on Windows-style line endings.
        if (!line.empty() && line.back() == '\r') line.pop_back();

        int balance = 0;
        bool valid = true;

        for (char c : line) {
            if (c == '(') {
                ++balance;
            } else if (c == ')') {
                if (balance == 0) {
                    valid = false;
                    break;
                }
                --balance;
            } else {
                // The specification guarantees only parentheses.
                // For safety, treat any other character as invalid.
                valid = false;
                break;
            }
        }

        if (valid && balance == 0) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}