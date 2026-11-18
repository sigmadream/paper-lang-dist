#include <iostream>
#include <string>

static bool isTrimChar(char c) {
    return static_cast<unsigned char>(c) <= ' ';
}

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) {
        return 0;
    }

    std::size_t begin = 0;
    while (begin < s.size() && isTrimChar(s[begin])) {
        ++begin;
    }

    std::size_t end = s.size();
    while (end > begin && isTrimChar(s[end - 1])) {
        --end;
    }

    s = s.substr(begin, end - begin);

    if (s.empty()) {
        return 0;
    }

    bool valid = true;
    for (std::size_t i = 0; i < s.size() / 2; ++i) {
        if (s[i] != s[s.size() - 1 - i]) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}