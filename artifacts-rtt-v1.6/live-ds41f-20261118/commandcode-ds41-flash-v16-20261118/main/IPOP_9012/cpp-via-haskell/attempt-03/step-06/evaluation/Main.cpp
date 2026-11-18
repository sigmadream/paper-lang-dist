#include <iostream>
#include <string>

static bool check(const std::string& s) {
    int bal = 0;
    for (char c : s) {
        if (c == '(') {
            ++bal;
        } else {
            if (bal <= 0) return false;
            --bal;
        }
    }
    return bal == 0;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    for (int i = 0; i < T; ++i) {
        std::string s;
        std::cin >> s;
        std::cout << (check(s) ? "YES" : "NO") << '\n';
    }

    return 0;
}