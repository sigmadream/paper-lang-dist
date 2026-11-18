#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s >> t)) {
        std::cout << 0 << '\n';
        return 0;
    }

    if (s.size() == t.size()) {
        std::sort(s.begin(), s.end());
        std::sort(t.begin(), t.end());
        std::cout << (s == t ? 1 : 0) << '\n';
    } else {
        std::cout << 0 << '\n';
    }

    return 0;
}