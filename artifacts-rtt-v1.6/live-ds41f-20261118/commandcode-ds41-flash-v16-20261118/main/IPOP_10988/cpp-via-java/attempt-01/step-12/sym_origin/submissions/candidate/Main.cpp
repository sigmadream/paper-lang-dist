#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) {
        return 0;
    }

    int begin = 0;
    int end = static_cast<int>(line.length());

    auto isSpace = [](char c) {
        return static_cast<unsigned char>(c) <= ' ';
    };

    while (begin < end && isSpace(line[begin])) {
        ++begin;
    }
    while (end > begin && isSpace(line[end - 1])) {
        --end;
    }

    if (begin >= end) {
        return 0;
    }

    bool valid = true;
    for (int i = begin; i < begin + (end - begin) / 2; ++i) {
        if (line[i] != line[end - 1 - (i - begin)]) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}