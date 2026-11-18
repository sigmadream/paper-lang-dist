#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s >> t)) {
        return 0;
    }

    int counts[26] = {0};

    for (char c : s) {
        counts[c - 'a']++;
    }

    for (char c : t) {
        counts[c - 'a']--;
    }

    for (int x : counts) {
        if (x != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}