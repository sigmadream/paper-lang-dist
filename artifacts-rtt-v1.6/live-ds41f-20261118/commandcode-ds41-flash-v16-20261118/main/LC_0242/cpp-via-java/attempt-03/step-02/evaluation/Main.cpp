#include <iostream>
#include <string>
#include <vector>

static std::string trim(const std::string& str) {
    size_t start = 0;
    size_t end = str.size();

    while (start < end && static_cast<unsigned char>(str[start]) <= ' ') {
        ++start;
    }

    while (end > start && static_cast<unsigned char>(str[end - 1]) <= ' ') {
        --end;
    }

    return str.substr(start, end - start);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s;
    std::string t;

    if (!std::getline(std::cin, s)) {
        s = "";
    }

    if (!std::getline(std::cin, t)) {
        t = "";
    }

    s = trim(s);
    t = trim(t);

    if (s.size() != t.size()) {
        std::cout << 0 << '\n';
        return 0;
    }

    int counts[26] = {0};

    for (size_t i = 0; i < s.size(); ++i) {
        ++counts[s[i] - 'a'];
        --counts[t[i] - 'a'];
    }

    for (int count : counts) {
        if (count != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}