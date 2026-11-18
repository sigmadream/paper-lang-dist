#include <iostream>
#include <string>
#include <cctype>
#include <array>

int main() {
    std::string s, t;

    if (!std::getline(std::cin, s)) {
        return 0;
    }

    if (!std::getline(std::cin, t)) {
        return 0;
    }

    auto trim = [](std::string& str) {
        size_t begin = 0;
        while (begin < str.size() && std::isspace(static_cast<unsigned char>(str[begin]))) {
            ++begin;
        }

        size_t end = str.size();
        while (end > begin && std::isspace(static_cast<unsigned char>(str[end - 1]))) {
            --end;
        }

        str = str.substr(begin, end - begin);
    };

    trim(s);
    trim(t);

    if (s.empty() || t.empty()) {
        return 0;
    }

    std::array<int, 26> counts{};

    for (char c : s) {
        ++counts[c - 'a'];
    }

    for (char c : t) {
        --counts[c - 'a'];
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