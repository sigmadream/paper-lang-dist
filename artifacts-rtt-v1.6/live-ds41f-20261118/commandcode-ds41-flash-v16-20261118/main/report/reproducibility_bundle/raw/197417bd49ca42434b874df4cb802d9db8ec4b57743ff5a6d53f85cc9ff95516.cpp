#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> data;
    std::string token;
    while (std::cin >> token) {
        data.push_back(token);
    }

    if (data.empty()) {
        return 0;
    }

    int t = std::stoi(data[0]);
    std::vector<std::string> answers;
    answers.reserve(t);

    for (int i = 1; i <= t; ++i) {
        const std::string& s = data[i];
        int balance = 0;
        bool valid = true;

        for (char ch : s) {
            if (ch == '(') {
                ++balance;
            } else {
                --balance;
            }

            if (balance < 0) {
                valid = false;
                break;
            }
        }

        if (balance != 0) {
            valid = false;
        }

        answers.push_back(valid ? "YES" : "NO");
    }

    for (const std::string& answer : answers) {
        std::cout << answer << '\n';
    }

    return 0;
}