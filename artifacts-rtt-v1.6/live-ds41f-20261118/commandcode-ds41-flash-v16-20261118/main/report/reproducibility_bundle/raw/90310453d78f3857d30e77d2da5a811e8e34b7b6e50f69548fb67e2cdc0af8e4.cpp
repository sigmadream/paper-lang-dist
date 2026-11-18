#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    auto readLine = []() {
        std::string line;
        if (!std::getline(std::cin, line)) {
            line = "";
        }
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        return line;
    };

    std::string s = readLine();
    std::string t = readLine();

    std::array<int, 26> counts{};

    for (char ch : s) {
        counts[ch - 'a']++;
    }
    for (char ch : t) {
        counts[ch - 'a']--;
    }

    bool valid = true;
    for (int c : counts) {
        if (c != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';

    return 0;
}