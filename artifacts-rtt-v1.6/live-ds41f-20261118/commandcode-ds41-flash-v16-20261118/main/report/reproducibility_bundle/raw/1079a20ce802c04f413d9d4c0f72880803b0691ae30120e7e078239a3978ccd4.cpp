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
    std::vector<std::string> out;

    for (int i = 0; i < t; ++i) {
        std::string s = (i + 1 < static_cast<int>(data.size())) ? data[i + 1] : "";
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

        out.push_back(valid ? "YES" : "NO");
    }

    for (size_t i = 0; i < out.size(); ++i) {
        std::cout << out[i];
        if (i + 1 < out.size()) {
            std::cout << '\n';
        }
    }
    if (!out.empty()) {
        std::cout << '\n';
    }

    return 0;
}