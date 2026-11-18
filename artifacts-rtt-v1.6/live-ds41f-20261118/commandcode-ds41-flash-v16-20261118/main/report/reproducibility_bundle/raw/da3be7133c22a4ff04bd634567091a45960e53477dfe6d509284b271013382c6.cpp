#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string s;
    std::getline(std::cin, s);

    // Strip whitespace (mirror Python's .strip())
    const std::string ws = " \t\n\r\f\v";
    size_t start = s.find_first_not_of(ws);
    if (start == std::string::npos) {
        s.clear();
    } else {
        size_t end = s.find_last_not_of(ws);
        s = s.substr(start, end - start + 1);
    }

    std::string rev(s.rbegin(), s.rend());
    std::cout << (s == rev ? 1 : 0) << '\n';
    return 0;
}