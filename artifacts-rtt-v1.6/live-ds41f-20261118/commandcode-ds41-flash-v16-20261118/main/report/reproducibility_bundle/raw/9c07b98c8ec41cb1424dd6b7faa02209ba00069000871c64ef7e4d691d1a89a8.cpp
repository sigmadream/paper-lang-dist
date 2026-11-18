#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> tokens;
    std::string token;
    while (std::cin >> token) {
        tokens.push_back(token);
    }

    if (tokens.empty()) {
        return 0;
    }

    int t = std::stoi(tokens[0]);
    std::vector<std::string> results;

    for (int i = 0; i < t; ++i) {
        std::string s = (static_cast<size_t>(i + 1) < tokens.size()) ? tokens[i + 1] : "";
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

        results.push_back(valid ? "YES" : "NO");
    }

    for (const auto& result : results) {
        std::cout << result << '\n';
    }

    return 0;
}