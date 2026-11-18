#include <algorithm>
#include <iostream>
#include <string>

static void read_line_codes(std::istream& in, std::string& out) {
    if (!std::getline(in, out)) {
        out.clear();
        return;
    }
    if (!out.empty() && out.back() == '\r') {
        out.pop_back();
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    read_line_codes(std::cin, s);
    read_line_codes(std::cin, t);

    std::sort(s.begin(), s.end());
    std::sort(t.begin(), t.end());

    std::cout << (s == t ? 1 : 0) << '\n';
    return 0;
}