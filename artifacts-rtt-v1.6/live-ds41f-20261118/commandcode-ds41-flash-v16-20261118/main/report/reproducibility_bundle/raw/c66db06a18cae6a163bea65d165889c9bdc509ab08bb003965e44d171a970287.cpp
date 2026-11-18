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
    std::vector<std::string> result;

    for (int i = 1; i <= t; ++i) {
        std::string s = (i < static_cast<int>(data.size())) ? data[i] : "";
        int balance = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') {
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

        result.push_back(valid ? "YES" : "NO");
    }

    for (int i = 0; i < static_cast<int>(result.size()); ++i) {
        if (i > 0) {
            std::cout << '\n';
        }
        std::cout << result[i];
    }

    return 0;
}