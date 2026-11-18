#include <iostream>
#include <string>
#include <array>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!std::getline(std::cin, s)) return 0;
    if (!std::getline(std::cin, t)) return 0;

    auto trim = [](std::string &str) {
        const std::string ws = " \t\n\r\f\v";
        std::size_t start = str.find_first_not_of(ws);
        if (start == std::string::npos) {
            str.clear();
            return;
        }
        std::size_t end = str.find_last_not_of(ws);
        str = str.substr(start, end - start + 1);
    };

    trim(s);
    trim(t);
    if (s.empty() || t.empty()) return 0;

    std::array<int, 26> counts{};
    for (char c : s) {
        counts[c - 'a']++;
    }
    for (char c : t) {
        counts[c - 'a']--;
    }

    bool valid = true;
    for (int count : counts) {
        if (count != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}