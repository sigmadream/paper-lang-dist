#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> data;
    string token;
    while (cin >> token) data.push_back(token);

    if (data.empty()) return 0;

    int t = stoi(data[0]);
    vector<string> answers;

    for (int i = 1; i <= t; ++i) {
        const string& s = data[i];
        int balance = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') ++balance;
            else --balance;

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) valid = false;

        answers.push_back(valid ? "YES" : "NO");
    }

    for (size_t i = 0; i < answers.size(); ++i) {
        if (i) cout << '\n';
        cout << answers[i];
    }

    return 0;
}