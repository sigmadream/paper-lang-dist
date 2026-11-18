#include <iostream>
#include <string>

int main() {
    std::string s;
    std::getline(std::cin, s);

    // Trim leading/trailing whitespace to mirror Python's strip()
    const std::string ws = " \t\n\r\f\v";
    std::size_t begin = s.find_first_not_of(ws);
    if (begin == std::string::npos) {
        s.clear();
    } else {
        std::size_t end = s.find_last_not_of(ws);
        s = s.substr(begin, end - begin + 1);
    }

    bool palindrome = true;
    for (std::size_t i = 0, j = s.size(); i + 1 < j; ++i, --j) {
        if (s[i] != s[j - 1]) {
            palindrome = false;
            break;
        }
    }

    std::cout << (palindrome ? 1 : 0) << '\n';
    return 0;
}