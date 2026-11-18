#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s)) return 0;
    if (!(std::cin >> t)) return 0;

    if (s.size() != t.size()) {
        std::cout << 0 << '\n';
        return 0;
    }

    std::vector<int> counts(26, 0);
    for (char c : s) counts[c - 'a']++;
    for (char c : t) counts[c - 'a']--;

    for (int v : counts) {
        if (v != 0) {
            std::cout << 0 << '\n';
            return 0;
        }
    }

    std::cout << 1 << '\n';
    return 0;
}