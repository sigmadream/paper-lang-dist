#include <iostream>
#include <string>
#include <array>

static bool isCppSpace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
}

static std::string trim(const std::string& str) {
    std::size_t begin = 0;
    while (begin < str.length() && isCppSpace(str[begin])) {
        ++begin;
    }

    std::size_t end = str.length();
    while (end > begin && isCppSpace(str[end - 1])) {
        --end;
    }

    return str.substr(begin, end - begin);
}

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }

    std::string t;
    if (!std::getline(std::cin, t)) {
        return 0;
    }

    s = trim(s);
    t = trim(t);

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