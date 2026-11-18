#include <iostream>
#include <string>

using namespace std;

static bool isWs(char c) {
    return c == '\t' || c == '\n' || c == '\v' ||
           c == '\f' || c == '\r' || c == ' ';
}

static string trim(const string& s) {
    size_t left = 0;
    size_t right = s.size();

    while (left < right && isWs(s[left])) {
        ++left;
    }
    while (right > left && isWs(s[right - 1])) {
        --right;
    }

    return s.substr(left, right - left);
}

static bool validParens(const string& s) {
    int balance = 0;

    for (char c : s) {
        if (c == '(') {
            ++balance;
        } else if (c == ')') {
            if (balance <= 0) {
                return false;
            }
            --balance;
        }
    }

    return balance == 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) {
        return 0;
    }

    string first = trim(line);
    int t = 0;

    try {
        t = stoi(first);
    } catch (...) {
        return 0;
    }

    for (int i = 0; i < t; ++i) {
        if (!getline(cin, line)) {
            return 0;
        }

        string trimmed = trim(line);
        cout << (validParens(trimmed) ? "YES" : "NO") << '\n';
    }

    return 0;
}