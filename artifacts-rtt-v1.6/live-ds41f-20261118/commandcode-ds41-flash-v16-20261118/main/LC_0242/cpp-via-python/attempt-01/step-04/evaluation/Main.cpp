#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s >> t)) return 0;

    std::vector<int> counts(26, 0);
    for (char ch : s) {
        counts[ch - 'a']++;
    }
    for (char ch : t) {
        counts[ch - 'a']--;
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