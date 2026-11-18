#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<std::string> data;
    std::string token;
    while (std::cin >> token) {
        data.push_back(token);
    }

    if (data.empty()) return 0;

    int t = std::stoi(data[0]);
    std::string output;

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

        output += valid ? "YES\n" : "NO\n";
    }

    std::cout << output;
    return 0;
}