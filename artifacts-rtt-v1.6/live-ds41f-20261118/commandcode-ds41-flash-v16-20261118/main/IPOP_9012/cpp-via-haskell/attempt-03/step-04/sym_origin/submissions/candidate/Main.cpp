#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string t;
    if (!(std::cin >> t)) return 0;

    int n = std::stoi(t);

    for (int i = 0; i < n; ++i) {
        std::string s;
        if (!(std::cin >> s)) break;

        int bal = 0;
        bool ok = true;

        for (char c : s) {
            if (c == '(') {
                ++bal;
            } else {
                if (bal > 0) {
                    --bal;
                } else {
                    ok = false;
                    break;
                }
            }
        }

        if (ok && bal == 0)
            std::cout << "YES\n";
        else
            std::cout << "NO\n";
    }

    return 0;
}