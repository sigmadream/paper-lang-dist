#include <iostream>
#include <string>

static std::string trim(const std::string &str) {
    int start = 0;
    int end = static_cast<int>(str.length());

    while (start < end && str[start] <= ' ') {
        ++start;
    }

    while (end > start && str[end - 1] <= ' ') {
        --end;
    }

    return str.substr(start, end - start);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    std::string s;
    std::string t;

    if (std::getline(std::cin, line)) {
        s = line;
    }

    if (std::getline(std::cin, line)) {
        t = line;
    }

    s = trim(s);
    t = trim(t);

    if (s.length() != t.length()) {
        std::cout << 0 << '\n';
        return 0;
    }

    int counts[26] = {0};

    for (std::size_t i = 0; i < s.length(); ++i) {
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