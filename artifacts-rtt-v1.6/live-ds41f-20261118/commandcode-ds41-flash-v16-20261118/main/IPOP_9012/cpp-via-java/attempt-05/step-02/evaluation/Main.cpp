#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    if (!(std::cin >> t)) return 0;

    std::string output;

    while (t-- > 0) {
        std::string s;
        std::cin >> s;

        int bal = 0;
        bool valid = true;

        for (char c : s) {
            if (c == '(') bal++;
            else bal--;

            if (bal < 0) {
                valid = false;
                break;
            }
        }

        if (bal != 0) valid = false;

        output += valid ? "YES\n" : "NO\n";
    }

    std::cout << output;
    return 0;
}