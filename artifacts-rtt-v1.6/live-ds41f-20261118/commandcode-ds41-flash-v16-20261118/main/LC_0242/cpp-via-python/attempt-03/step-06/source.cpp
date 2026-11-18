#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s)) return 0;
    if (!(std::cin >> t)) return 0;

    int count[26] = {0};

    for (char c : s) {
        count[c - 'a']++;
    }

    for (char c : t) {
        count[c - 'a']--;
    }

    for (int x : count) {
        if (x != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}