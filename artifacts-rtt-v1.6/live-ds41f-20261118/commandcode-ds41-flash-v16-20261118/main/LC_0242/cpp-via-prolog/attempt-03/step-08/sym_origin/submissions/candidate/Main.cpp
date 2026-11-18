#include <iostream>
#include <string>
#include <algorithm>

static std::string strip_trailing_cr(std::string s) {
    if (!s.empty() && s.back() == '\r') s.pop_back();
    return s;
}

static bool read_line_codes(std::string &s) {
    if (!std::getline(std::cin, s)) {
        s.clear();
        return false;
    }
    s = strip_trailing_cr(s);
    return true;
}

int main() {
    std::string s, t;
    read_line_codes(s);
    read_line_codes(t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}