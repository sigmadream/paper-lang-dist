#include <iostream>
#include <string>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    std::size_t begin = 0;
    std::size_t end = line.size();

    while (begin < end && line[begin] <= ' ') {
        ++begin;
    }
    while (end > begin && line[end - 1] <= ' ') {
        --end;
    }

    std::string s = line.substr(begin, end - begin);
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