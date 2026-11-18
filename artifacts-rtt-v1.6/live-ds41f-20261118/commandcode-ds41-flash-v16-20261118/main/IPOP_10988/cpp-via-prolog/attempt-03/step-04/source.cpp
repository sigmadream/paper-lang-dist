#include <iostream>
#include <string>

int main() {
    std::string s;
    if (!std::getline(std::cin, s)) return 0;
    // normalize: trim leading and trailing whitespace
    size_t start = 0, end = s.size();
    while (start < end && std::isspace(static_cast<unsigned char>(s[start]))) ++start;
    while (end > start && std::isspace(static_cast<unsigned char>(s[end - 1]))) --end;
    s = s.substr(start, end - start);
    if (s.empty()) return 0;
    bool ok = true;
    for (size_t i = 0, j = s.size() - 1; i < j; ++i, --j) {
        if (s[i] != s[j]) { ok = false; break; }
    }
    std::cout << (ok ? 1 : 0) << '\n';
    return 0;
}