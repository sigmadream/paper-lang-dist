#include <iostream>
#include <string>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string s, t;
    if (!(std::cin >> s)) return 0;
    if (!(std::cin >> t)) return 0;

    std::vector<int> counts(26, 0);
    for (char ch : s) {
        counts[ch - 'a'] += 1;
    }
    for (char ch : t) {
        counts[ch - 'a'] -= 1;
    }

    bool valid = true;
    for (int c : counts) {
        if (c != 0) {
            valid = false;
            break;
        }
    }

    std::cout << (valid ? 1 : 0) << '\n';
    return 0;
}